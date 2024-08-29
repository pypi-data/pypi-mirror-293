import importlib
import json
import os
import uuid
from multiprocessing import Process

import zmq

from .log_utils import LogIssuer, tprint
from .slide_worker import SlideWorker
from .worker_cache import WorkerCache

POLLER_TIMEOUT_SECONDS = 15


def _initialize_worker_process(
    plugin_module: str, plugin_class_name: str, filepath: str, worker_id: str, tcp_port: int
):
    module = importlib.import_module(name=f"{plugin_module}.slide", package=".")
    plugin_instance = getattr(module, plugin_class_name)
    slide_worker = SlideWorker(
        mapped_filepath=filepath, slide_instance_type=plugin_instance, worker_id=worker_id, tcp_port=tcp_port
    )
    slide_worker.run()


class BackendServer:
    """BackendServer"""

    def __init__(self, plugin_module: str, plugin_class_name: str, tcp_port: int = 5556):
        self.verbose_logging = (
            (not bool(os.getenv("PLUGIN_ENABLE_DEBUG"))) if os.getenv("PLUGIN_ENABLE_DEBUG") else False
        )
        tprint(issuer=LogIssuer.MAIN, msg="Initializing plugin...", verbose_logging=True)
        self._plugin_module = plugin_module
        self._plugin_class_name = plugin_class_name
        self._client_tcp_port = tcp_port
        self._worker_cache = WorkerCache()

    def run(self):
        context: zmq.Context = zmq.Context()
        client_socket: zmq.Socket = context.socket(zmq.ROUTER)
        client_socket.bind(f"tcp://*:{self._client_tcp_port}")
        tprint(
            issuer=LogIssuer.MAIN,
            msg=f"Zeromq server binding to 'tcp://*:{self._client_tcp_port}'",
            verbose_logging=True,
        )

        poller: zmq.Poller = zmq.Poller()
        poller.register(socket=client_socket, flags=zmq.POLLIN)

        while True:
            sockets = poller.poll(POLLER_TIMEOUT_SECONDS)
            if not sockets:
                self.__cleanup_expired_workers()
                continue

            for socket, _ in sockets:
                msg = socket.recv_multipart()
                client_id = msg[0].decode("ascii")
                req_msg = json.loads(msg[1])

                if req_msg.get("req") == "ALIVE":
                    client_socket.send_string(client_id, zmq.SNDMORE)
                    client_socket.send_json({"is_alive": True})
                    continue

                if socket == client_socket:
                    self.__handle_client_request(context, poller, client_id, req_msg)
                else:
                    client_socket.send_multipart(msg)

    def __cleanup_expired_workers(self):
        expired_filepath_sockets = self._worker_cache.get_expired_filepath_sockets()
        for expired_filepath_socket in expired_filepath_sockets.keys():
            num_workers = self._worker_cache.get_worker_count(expired_filepath_socket)

            exp_socket: zmq.Socket
            exp_socket, _ = expired_filepath_sockets[expired_filepath_socket]
            for _ in range(num_workers):
                exp_socket.send_string("SIGNAL", zmq.SNDMORE)
                exp_socket.send_json({"req": "KILL_PROC"})

            self._worker_cache.clear_cache_items(expired_filepath_socket)

    def __handle_client_request(self, context: zmq.Context, poller: zmq.Poller, client_id: str, req_msg: dict):
        filepath = req_msg.get("filepath")
        min_workers = req_msg.get("min_workers", 1)

        filepath_socket, filepath_port = self._worker_cache.get_socket(filepath=filepath)
        if filepath_socket is None:
            filepath_socket: zmq.Socket = context.socket(zmq.DEALER)
            filepath_port = filepath_socket.bind_to_random_port("tcp://0.0.0.0")
            poller.register(socket=filepath_socket, flags=zmq.POLLIN)

            self._worker_cache.add_socket(filepath=filepath, socket=filepath_socket, port=filepath_port)

        num_workers = self._worker_cache.get_worker_count(filepath=filepath)
        diff_workers = min_workers - num_workers
        diff_workers = max(diff_workers, 0)

        for _ in range(diff_workers):
            worker_id = str(uuid.uuid4())
            process = Process(
                target=_initialize_worker_process,
                args=(self._plugin_module, self._plugin_class_name, filepath, worker_id, filepath_port),
            )
            process.start()
            self._worker_cache.add_worker(filepath=filepath, worker_id=worker_id)

        filepath_socket.send_string(client_id, zmq.SNDMORE)
        filepath_socket.send_json(req_msg)

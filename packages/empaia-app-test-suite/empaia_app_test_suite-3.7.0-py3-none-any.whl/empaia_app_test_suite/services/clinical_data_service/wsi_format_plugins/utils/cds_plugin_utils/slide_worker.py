import threading
from typing import Dict, Type

import zmq

from .base_slide_instance import BaseSlideInstance
from .log_utils import LogIssuer, tprint


class SlideWorker(threading.Thread):
    """SlideWorker"""

    def __init__(
        self,
        mapped_filepath: str,
        slide_instance_type: Type[BaseSlideInstance],
        worker_id: str,
        tcp_port: int,
        verbose_logging: bool = False,
    ):
        self._mapped_filepath = mapped_filepath
        self._slide_instance: BaseSlideInstance = slide_instance_type(self._mapped_filepath)
        self._worker_id = worker_id
        self._tcp_port = tcp_port
        self._verbose_logging = verbose_logging
        tprint(issuer=LogIssuer.WORKER, msg=f"Initialized worker for slide {mapped_filepath}", verbose_logging=True)

    def run(self):
        context: zmq.Context = zmq.Context()
        socket: zmq.Socket = context.socket(zmq.DEALER)
        socket.connect(f"tcp://127.0.0.1:{self._tcp_port}")

        while True:
            client_id = socket.recv_string()
            req_msg = socket.recv_json()
            tprint(
                issuer=LogIssuer.WORKER,
                msg=f"Received request from {client_id}: {req_msg}",
                verbose_logging=self._verbose_logging,
            )
            if client_id == "SIGNAL" and req_msg["req"] == "KILL_PROC":
                tprint(
                    issuer=LogIssuer.WORKER,
                    msg=f"Received kill signal. Closing socket connection for {self._mapped_filepath}...",
                    verbose_logging=self._verbose_logging,
                )
                socket.close()
                break
            elif req_msg["req"] == "CHECK_IS_SUPPORTED":
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=self._slide_instance.result,
                )
            elif req_msg["req"] == "SLIDE_INFO":
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=self._slide_instance.get_info(),
                )
            elif req_msg["req"] == "LABEL":
                resp, image_array = self._slide_instance.get_label(
                    max_x=req_msg["max_x"],
                    max_y=req_msg["max_y"],
                    image_format=req_msg["image_format"],
                    image_quality=req_msg["image_quality"],
                )
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=resp,
                    image_array=image_array,
                )
            elif req_msg["req"] == "MACRO":
                resp, image_array = self._slide_instance.get_macro(
                    max_x=req_msg["max_x"],
                    max_y=req_msg["max_y"],
                    image_format=req_msg["image_format"],
                    image_quality=req_msg["image_quality"],
                )
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=resp,
                    image_array=image_array,
                )
            elif req_msg["req"] == "REGION":
                resp, image_array = self._slide_instance.get_region(
                    level=req_msg["level"],
                    start_x=req_msg["start_x"],
                    start_y=req_msg["start_y"],
                    size_x=req_msg["size_x"],
                    size_y=req_msg["size_y"],
                    image_format=req_msg["image_format"],
                    image_quality=req_msg["image_quality"],
                    image_channels=req_msg["image_channels"],
                    padding_color=tuple(req_msg["padding_color"]),
                    z=req_msg["z"],
                )
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=resp,
                    image_array=image_array,
                )
            elif req_msg["req"] == "TILE":
                resp, image_array = self._slide_instance.get_tile(
                    level=req_msg["level"],
                    tile_x=req_msg["tile_x"],
                    tile_y=req_msg["tile_y"],
                    image_format=req_msg["image_format"],
                    image_quality=req_msg["image_quality"],
                    image_channels=req_msg["image_channels"],
                    padding_color=tuple(req_msg["padding_color"]),
                    z=req_msg["z"],
                )
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=resp,
                    image_array=image_array,
                )
            elif req_msg["req"] == "THUMBNAIL":
                resp, image_array = self._slide_instance.get_thumbnail(
                    max_x=req_msg["max_x"],
                    max_y=req_msg["max_y"],
                    image_format=req_msg["image_format"],
                    image_quality=req_msg["image_quality"],
                )
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data=resp,
                    image_array=image_array,
                )
            else:
                req = req_msg["req"]
                self.__send_array_response(
                    socket=socket,
                    client_id=client_id,
                    data={
                        "rep": "error",
                        "status_code": 422,
                        "detail": f"Invalid request ({req})",
                    },
                )

        self._slide_instance.close()

    def __send_array_response(self, socket: zmq.Socket, client_id: str, data: Dict, image_array: bytes = None):
        if image_array is None:
            image_array = b""

        socket.send_string(client_id, zmq.SNDMORE)
        socket.send_json(data, zmq.SNDMORE)
        socket.send(image_array)

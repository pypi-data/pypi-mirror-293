import threading

import zmq

from .log_utils import LogIssuer, tprint


class ResponseHandler(threading.Thread):
    def __init__(self, incoming_router_socket: zmq.Socket, broker_socket: zmq.Socket, verbose_logging: bool = False):
        threading.Thread.__init__(self)
        self.incoming_router_socket = incoming_router_socket
        self.broker_socket = broker_socket
        self.verbose_logging = verbose_logging
        tprint(issuer=LogIssuer.RESP_HANDLER, msg=f"Initialized response handler", verbose_logging=True)

    def run(self):
        while True:
            # route response to frontend socket
            response = self.broker_socket.recv_multipart()
            response.pop(0)
            tprint(
                issuer=LogIssuer.RESP_HANDLER,
                msg=f"Forwarding message to {response[0]}: {response[1][:100]}...",
                verbose_logging=self.verbose_logging,
            )
            self.incoming_router_socket.send_multipart(response)

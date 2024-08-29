import time

EXPIRATION_TIME_SECONDS = 300


class WorkerCache:
    def __init__(self):
        self._worker_ids = {}
        self._sockets = {}

    def add_worker(self, filepath, worker_id):
        worker_ids = self._worker_ids.get(filepath, [])
        worker_ids.append(worker_id)
        self._worker_ids[filepath] = worker_ids

    def add_socket(self, filepath, socket, port):
        expiration_time = time.time() + EXPIRATION_TIME_SECONDS
        self._sockets[filepath] = (socket, port, expiration_time)

    def get_socket(self, filepath):
        socket, port, expiration_time = self._sockets.get(filepath, (None, None, None))
        if socket:
            expiration_time = time.time() + EXPIRATION_TIME_SECONDS
            self._sockets[filepath] = (socket, port, expiration_time)

        return (socket, port)

    def get_expired_filepath_sockets(self):
        expired_items = {}
        for key in self._sockets.keys():
            socket, port, expiration_time = self._sockets[key]
            if time.time() > expiration_time:
                expired_items[key] = (socket, port)
        return expired_items

    def get_worker_count(self, filepath):
        worker_ids = self._worker_ids.get(filepath, [])
        return len(worker_ids)

    def clear_cache_items(self, filepath):
        self._worker_ids.pop(filepath)
        self._sockets.pop(filepath)

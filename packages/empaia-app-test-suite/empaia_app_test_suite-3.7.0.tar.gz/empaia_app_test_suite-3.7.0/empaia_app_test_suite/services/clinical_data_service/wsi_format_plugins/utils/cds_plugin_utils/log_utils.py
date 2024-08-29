import sys
from enum import Enum


class LogIssuer(str, Enum):
    MAIN = "Main thread"
    RESP_HANDLER = "Response Handler"
    WORKER = "Worker thread"
    CACHE = "Cache"


def tprint(issuer: LogIssuer, msg: str, verbose_logging: bool = False):
    """like print, but won't get newlines confused with multiple threads"""
    if verbose_logging:
        sys.stdout.write(f"{issuer} | {msg}\n")
        sys.stdout.flush()

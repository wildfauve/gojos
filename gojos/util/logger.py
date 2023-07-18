from typing import Dict, Optional, Union, Tuple
from enum import Enum
# from pino import pino
# import sys
# from functools import reduce
import rich
import time

print_fn = rich.print


class LogType(Enum):
    PERF_LOG = "perflog"
    DEBUG = "debug"
    INFO = "info"


logging_switch = {
    LogType.PERF_LOG: True,
    LogType.DEBUG: True,
    LogType.INFO: False
}


def log(entry, log_type: LogType = LogType.INFO):
    if logging_switch[log_type]:
        print_fn(entry)


def debug(entry):
    log(entry, LogType.DEBUG)


def info(entry):
    log(entry, LogType.INFO)


def with_perf_log(perf_log_type: str = None, name: str = None):
    """
    Decorator which wraps the fn in a timer and writes a performance log
    """

    def inner(fn):
        def invoke(*args, **kwargs):
            t1 = time.time()
            result = fn(*args, **kwargs)
            t2 = time.time()
            fn_name = kwargs['name'] if 'name' in kwargs else name or fn.__name__
            perf_log(fn=f"{fn_name} ctx: {kwargs.get('perf_ctx', None)}", delta_t=(t2 - t1) * 1000.0)
            return result

        return invoke

    return inner


def perf_log(fn: str, delta_t: float):
    log(f"PerfLog: delta_t: {delta_t}, fn: {fn}", log_type=LogType.PERF_LOG)

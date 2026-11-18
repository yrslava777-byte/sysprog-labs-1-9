import argparse
import ctypes as C
import errno
import json
import os
from pathlib import Path
import sys


class CoreInfo(C.Structure):
    _fields_ = [
        ("pid", C.c_int64),
        ("cpus", C.c_int32),
        ("page_size", C.c_int32),
        ("host", C.c_char * 256),
    ]


def load_core(path):
    core = C.CDLL(str(path.resolve()))
    core.core_get_info.argtypes = [C.POINTER(CoreInfo)]
    core.core_get_info.restype = C.c_int
    return core


def get_info(core):
    info = CoreInfo()
    error = core.core_get_info(C.byref(info))
    if error:
        raise OSError(error, os.strerror(error))
    return {
        "event": "agent_started",
        "pid": info.pid,
        "cpus": info.cpus,
        "page_size": info.page_size,
        "host": info.host.decode("utf-8", errors="replace"),
    }


def main():
    name = "libsentry_core.dylib" if sys.platform == "darwin" else "libsentry_core.so"
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", type=Path, default=Path(__file__).resolve().parents[1] / "core" / name)
    parser.add_argument("--check-null", action="store_true")
    parser.add_argument("--layout", action="store_true")
    args = parser.parse_args()
    core = load_core(args.library)
    if args.check_null:
        error = core.core_get_info(None)
        print(f"NULL: {error} ({os.strerror(error)})")
        return 0 if error == errno.EINVAL else 1
    if args.layout:
        offsets = [getattr(CoreInfo, field).offset for field, _ in CoreInfo._fields_]
        print(f"sizeof: {C.sizeof(CoreInfo)}, offsets: {' '.join(map(str, offsets))}")
        return 0
    print(json.dumps(get_info(core), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

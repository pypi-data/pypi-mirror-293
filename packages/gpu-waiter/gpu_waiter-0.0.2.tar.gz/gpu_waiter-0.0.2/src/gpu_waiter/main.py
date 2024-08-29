"""Test config"""

import argparse
import os

from . import NVGPU, Tasker, Waiter


def get_args() -> argparse.Namespace:
    """Init argument and parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mem", type=str, default="24GB", help="memory size required"
    )
    parser.add_argument(
        "-g", "--gpu", type=int, default=1, help="amount of gpu required"
    )
    parser.add_argument(
        "-s",
        "--single_user",
        action="store_true",
        help="not use gpu if already has user",
    )
    parser.add_argument("-c", "--cmd", type=str, required=True, help="command to run")
    parser.add_argument(
        "-t", "--time", type=int, default=2, help="time of peried between check"
    )
    parser.add_argument("-vvv", "--verbose", action="store_true", help="dump all log")
    return parser.parse_args()


def main():
    """Execute"""
    args = get_args()

    nv = None
    if args.gpu:
        nv = NVGPU(
            args.gpu,
            args.mem,
            args.single_user,
        )

    task = Tasker(
        args.cmd,
        msg_level=1 if args.verbose else 2,
        devices=nv,
    )
    wt = Waiter(args.time, task)
    wt.do_wait()


if __name__ == "__main__":
    main()

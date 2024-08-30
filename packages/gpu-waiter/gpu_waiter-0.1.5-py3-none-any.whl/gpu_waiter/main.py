"""Test config"""

import argparse

from . import NVGPU, Tasker, Waiter


def get_args() -> argparse.Namespace:
    """Init argument and parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--cmd",
        type=str,
        default="",
        help="""command to run; -c could to be not specified; -c could be ignored but command should be posed at the end of shell sentence; command could be not string only if -c is ignored.""",
    )
    parser.add_argument(
        "-g", "--gpu", type=int, default=1, help="amount of gpu required."
    )
    parser.add_argument(
        "-m", "--mem", type=str, default="24GB", help="memory size required."
    )
    parser.add_argument(
        "-s",
        "--single_user",
        action="store_true",
        help="not use gpu if already has user.",
    )
    parser.add_argument(
        "-t", "--time", type=int, default=2, help="time of peried between check."
    )
    parser.add_argument("-vvv", "--verbose", action="store_true", help="dump all log.")
    args, argsv = parser.parse_known_args()
    if not args.cmd:
        assert argsv, "command content should be set and not be empty\n"+parser.format_help()
        args.cmd = []
        for i in argsv:
            args.cmd.extend(i.split(" "))
    else:
        assert not argsv, parser.format_help()
    return args


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

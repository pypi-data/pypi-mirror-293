"""tasker Module"""

import logging
import sys
import traceback
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import Callable, TextIO

from . import DEVICE


# pylint: disable=R0913
class Tasker:
    """
    command or function warp into task with necessary devices
    """

    def __init__(
        self,
        command: list | str | Callable,
        stdout=None,
        msg_level: int = 2,
        log_format="%(message)s",
        tag="",
        devices: list[DEVICE] = None,
        *args,
        **kwargs
    ):
        """_summary_

        Args:
            command (list | str | Callable):
                command of task, could be list|str|function point,
                but function point would not support logger.
                !!! if command is function, it shuold have a key named !!!
                !!! "logger" in it's params to get tasker logger in    !!!
            stdout (_type_, optional):
                stdout redirect. Defaults to None.
            stderr (_type_, optional):
                stderr redirect. Defaults to None.
            msg_level (int, optional):
                msg_level of information. Defaults to 3.
                the lower, the more information will be print
            devices (list[DEVICE], optional):
                task requires devices to run, devices should extend
                from class DEVICE. Defaults to [].
        """
        # log_format = logging.Formatter(
        #     "%(asctime)s %(filename)s[:%(lineno)d] [%(levelname)s]: %(message)s"
        # )
        self.log_format = logging.Formatter(log_format)
        self.init_logger(stdout, int(msg_level * 10), tag)
        self.args = args
        self.kwargs = kwargs

        if isinstance(command, str):
            self.command = command.split(' ')
        elif isinstance(command, list) or isinstance(command, Callable):
            self.command = command

        self.devices = []
        self.set_device(devices)
        self.finish = False

    def add_devices(self, devices):
        if not isinstance(devices, list):
            devices = [devices]
        for i in devices:
            assert isinstance(i, DEVICE)
            self.devices.append(i)

    def set_device(self, devices):
        if not devices:
            devices = []
        if not isinstance(devices, list):
            devices = [devices]
        for i in devices:
            assert isinstance(i, DEVICE)
        self.devices = devices

    def check(self):
        for device in self.devices:
            if not device.check():
                return False
        return True

    def __str__(self):
        return str(self.command)

    def do_task(self):
        try:
            if isinstance(self.command, Callable):
                self.stdout.warning("callable method does not support to set stdout")
                return self.command(logger=self.logger, *self.args, **self.kwargs)
            elif isinstance(self.command, list):
                process = Popen(
                    self.command,
                    stdout=PIPE,
                    # stderr=PIPE,
                    stderr=STDOUT,
                    *self.args,
                    **self.kwargs,
                )
                with process.stdout as process_stdout:
                    for line in iter(process_stdout.readline, b""):
                        self.logger.info(line.decode("utf8").strip("\n"))
            self.finish = True
        except Exception as e:
            traceback.print_exc(e)

    def get_handler(self, std=None, level=logging.WARNING):

        if isinstance(std, str) or isinstance(std, Path):
            handler = logging.FileHandler(std)
        elif isinstance(std, TextIO):
            handler = logging.StreamHandler(std)
        else:
            handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.log_format)
        handler.setLevel(level)
        return handler

    def init_logger(self, logger=None, level=30, tag=""):
        self.logger = logging.getLogger("task_logger" if not tag else tag)
        self.logger.setLevel(level)
        self.logger.addHandler(
            (
                self.get_handler(logger, level=level)
                if not logger
                else self.get_handler(sys.stdout, level=level)
            )
        )

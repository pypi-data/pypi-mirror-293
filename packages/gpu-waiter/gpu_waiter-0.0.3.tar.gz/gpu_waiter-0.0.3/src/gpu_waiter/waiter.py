"""waiter Module"""

import logging
import sys
import traceback
from time import sleep

from .device import DEVICE
from .tasker import Tasker


class Waiter:
    """
    a waiter to wait for satisified device to excute tasker
    """

    __TASKER_LIST__ = []

    def __init__(self, period: int = 5, taskers: Tasker | list = None):
        """_summary_

        Args:
            period (int, optional): period to check tasker. Defaults to 5.
            taskers (Tasker | list, optional): taskers to run. Defaults to None.
        """
        self.period = period
        if not taskers:
            taskers = []
        self.add_task(taskers)
        self.logger = logging.getLogger("wait_logger")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(filename)s[:%(lineno)d] [%(levelname)s]: %(message)s"
            )
        )
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def add_task(self, taskers: Tasker | list):
        """add tasker to waiter

        Args:
            taskers (Tasker | list): tasker or tasker list
        """
        
        if not isinstance(taskers, list):
            taskers = [taskers]
        for tasker in taskers:
            assert isinstance(tasker, Tasker)
            self.__TASKER_LIST__.append(tasker)

    def do_wait(self):
        """excute waiter"""
        while self.__TASKER_LIST__:
            self.logger.info("wait for task satisfied")
            sleep(self.period)
            for task in self.__TASKER_LIST__:
                try:
                    if task.check():
                        self.logger.info(str(task) + " excuting...")
                        task.do_task()
                        self.__TASKER_LIST__.remove(task)
                except Exception as e:
                    traceback.print_exc(e)


# pylint: disable=R0913
def waiter(
    stdout=None,
    msg_level: int = 3,
    log_format="%(message)s",
    tag="",
    devices: list[DEVICE] = None,
    period=5,
):
    """this is a detector, with the same function of Waiter

    Args:
        stdout (_type_, optional): _description_. Defaults to None.
        msg_level (int, optional): _description_. Defaults to 3.
        log_format (str, optional): _description_. Defaults to "%(message)s".
        tag (str, optional): _description_. Defaults to "".
        devices (list[DEVICE], optional): _description_. Defaults to [].
        period (int, optional): _description_. Defaults to 5.
    """
    if not devices:
        devices = []

    def decorator(func):
        def wrapper(*args, **kwargs):

            tasker = Tasker(
                func, stdout, msg_level, log_format, tag, devices, *args, **kwargs
            )

            while True:
                if tasker.check():
                    result = tasker.do()
                sleep(period)
            return result

        return wrapper

    return decorator

"""gpu-waiter"""
__version__ = '0.0.3'
from device import DEVICE, NVGPU
from .tasker import Tasker
from .utils import convertFileSize
from .waiter import Waiter

__all__ = [
    "Waiter", "Tasker", "DEVICE", "NVGPU", "convertFileSize"
]

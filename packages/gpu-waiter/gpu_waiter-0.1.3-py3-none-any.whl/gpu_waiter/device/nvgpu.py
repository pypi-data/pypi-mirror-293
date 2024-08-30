import heapq
import os

from nvitop import Device, GpuProcess

from ..utils import convertFileSize
from .device import DEVICE


class NVGPU(DEVICE):
    __SYS_REV_MEM__ = convertFileSize("200MiB")

    def __init__(
        self, count: int = 1, memory: float | str = "23GiB", single_user: bool = True
    ):
        self.count = count
        self.memory = convertFileSize(memory) if isinstance(memory, str) else memory
        self.single_user = single_user

    @property
    def devices(self):
        return Device.all()

    def device_check(self, device):
        if not convertFileSize(device.memory_free_human()) > self.memory:
            return False
        if self.single_user:
            processes = device.processes()
            if not len(processes):
                return True
            processes = GpuProcess.take_snapshots(processes.values(), failsafe=True)
            for process in processes:
                if convertFileSize(process.gpu_memory()) > self.__SYS_REV_MEM__:
                    return False
        return True

    def check(self):
        avilable_device = []
        for device in self.devices:
            if self.device_check(device):
                avilable_device.append(device)
        if len(avilable_device) >= self.count:
            self.set_device_env(avilable_device)
            return True
        else:
            return False

    def set_device_env(self, devices):
        if len(devices) > self.count:
            freemem = [
                convertFileSize(device.memory_free_human()) for device in devices
            ]
            top_index = heapq.nlargest(
                self.count, range(len(freemem)), freemem.__getitem__
            )
            devices = [devices[i] for i in top_index]
        device_index = [str(device.index) for device in devices]
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(device_index)

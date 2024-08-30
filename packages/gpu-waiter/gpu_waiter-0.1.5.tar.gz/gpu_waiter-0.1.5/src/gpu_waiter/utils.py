import time
import traceback

from nvitop import NA, Device, GpuProcess, colored


def convertFileSize(size):
    # 定义单位列表
    units = ["k", "m", "g", "t", "p"]
    # 循环判断文件大小是否大于1024，如果大于则转换为更大的单位
    try:
        size = size.lower()
        for scale, i in enumerate(units, 1):
            if i in size:
                return float(size.split(i)[0]) * (1000**scale)
        return float(size)
    except Exception as e:
        traceback.print_exc(e)
    return 0


if __name__ == "__main__":
    devices = Device.all()  # or `Device.cuda.all()` to use CUDA ordinal instead
    for device in devices:
        processes = device.processes()  # type: Dict[int, GpuProcess]
        sorted_pids = sorted(processes.keys())

        print(device)
        print(f"  - Fan speed:       {device.fan_speed()}%")
        print(f"  - Temperature:     {device.temperature()}C")
        print(f"  - GPU utilization: {device.gpu_utilization()}%")
        print(f"  - Total memory:    {device.memory_total_human()}")
        print(f"  - Used memory:     {device.memory_used_human()}")
        print(f"  - Free memory:     {device.memory_free_human()}")
        print(f"  - Processes ({len(processes)}): {sorted_pids}")
        for pid in sorted_pids:
            print(f"    - {processes[pid]}")
        print("-" * 120)

    print(colored(time.strftime("%a %b %d %H:%M:%S %Y"), color="red", attrs=("bold",)))

    devices = Device.cuda.all()  # or `Device.all()` to use NVML ordinal instead
    separator = False
    for device in devices:
        processes = device.processes()  # type: Dict[int, GpuProcess]

        print(colored(str(device), color="green", attrs=("bold",)))
        print(
            colored("  - Fan speed:       ", color="blue", attrs=("bold",))
            + f"{device.fan_speed()}%"
        )
        print(
            colored("  - Temperature:     ", color="blue", attrs=("bold",))
            + f"{device.temperature()}C"
        )
        print(
            colored("  - GPU utilization: ", color="blue", attrs=("bold",))
            + f"{device.gpu_utilization()}%"
        )
        print(
            colored("  - Total memory:    ", color="blue", attrs=("bold",))
            + f"{device.memory_total_human()}"
        )
        print(
            colored("  - Used memory:     ", color="blue", attrs=("bold",))
            + f"{device.memory_used_human()}"
        )
        print(
            colored("  - Free memory:     ", color="blue", attrs=("bold",))
            + f"{device.memory_free_human()}"
        )
        if len(processes) > 0:
            processes = GpuProcess.take_snapshots(processes.values(), failsafe=True)
            processes.sort(key=lambda process: (process.username, process.pid))

            print(
                colored(
                    f"  - Processes ({len(processes)}):", color="blue", attrs=("bold",)
                )
            )
            fmt = "    {pid:<5}  {username:<8} {cpu:>5}  {host_memory:>8} {time:>8}  {gpu_memory:>8}  {sm:>3}  {command:<}".format
            print(
                colored(
                    fmt(
                        pid="PID",
                        username="USERNAME",
                        cpu="CPU%",
                        host_memory="HOST-MEM",
                        time="TIME",
                        gpu_memory="GPU-MEM",
                        sm="SM%",
                        command="COMMAND",
                    ),
                    attrs=("bold",),
                )
            )
            for snapshot in processes:
                print(
                    fmt(
                        pid=snapshot.pid,
                        username=snapshot.username[:7]
                        + (
                            "+"
                            if len(snapshot.username) > 8
                            else snapshot.username[7:8]
                        ),
                        cpu=snapshot.cpu_percent,
                        host_memory=snapshot.host_memory_human,
                        time=snapshot.running_time_human,
                        gpu_memory=(
                            snapshot.gpu_memory_human
                            if snapshot.gpu_memory_human is not NA
                            else "WDDM:N/A"
                        ),
                        sm=snapshot.gpu_sm_utilization,
                        command=snapshot.command,
                    )
                )
        else:
            print(colored("  - No Running Processes", attrs=("bold",)))

        if separator:
            print("-" * 120)
        separator = True

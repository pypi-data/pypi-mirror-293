# gpu-waiter

## 1. Overview

gpu device moniter and automaticly run commond if device available, just for nvidia gpu.

## 2. Usage

### 2.1 init project

```bash
git clone https://github.com/lijunjie2232/gpu_waiter.git
pip install nvitop
pip install .
```

### 2.2 usage


```bash
$ waiter -h
usage: task-waiter [-h] [-m MEM] [-g GPU] [-s] -c CMD [-t TIME] [-vvv]

options:
  -h, --help            show this help message and exit
  -m MEM, --mem MEM     memory size required
  -g GPU, --gpu GPU     amount of gpu required
  -s, --single_user     not use gpu if already has user
  -c CMD, --cmd CMD     command to run
  -t TIME, --time TIME  time of peried between check
  -vvv, --verbose       dump all log
```

```python
#/bin/bash
from gpu_waiter import Tasker, Waiter
from gpu_waiter import NVGPU

if __name__ == "__main__":
    nv = NVGPU(2, "23GiB", False)
    nv.check()

    task = Tasker(
        [
            "ls",
            "-alh",
            "/usr/local/",
        ],
        msg_level=1,
        devices=nv
    )

    wt = Waiter(3, task)
    wt.do_wait()
    
    wt = Waiter(3)
    wt.add_task(task)
    wt.add_task(task)
    wt.do_wait()

```

## 3. Develop

---
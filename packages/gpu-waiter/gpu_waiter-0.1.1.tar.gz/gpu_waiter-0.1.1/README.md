# gpu-waiter

## 1. Overview

gpu device moniter and automaticly run commond if device available, just for nvidia gpu.

## 2. Install & Usage

### 2.1 install

```bash
pip install gpu-waiter
```

### 2.2 usage


```bash
$ waiter -g 2 -m 40G ls -alh /usr/local
$ waiter -g 2 -m 40G -c ls -alh /usr/local
$ waiter -g 2 -m 40G -c "ls -alh /usr/local"
$ waiter -c "ls -alh /usr/local" -g 2 -m 40G

$ waiter -h
usage: waiter [-h] [-c CMD] [-g GPU] [-m MEM] [-s] [-t TIME] [-vvv]

options:
  -h, --help            show this help message and exit.
  -c CMD, --cmd CMD     command to run; -c could to be not specified; -c could be ignored but command should be posed at the end of shell setence; command
                        could be not string only if -c is ignored.
  -g GPU, --gpu GPU     amount of gpu required.
  -m MEM, --mem MEM     memory size required.
  -s, --single_user     not use gpu if already has user.
  -t TIME, --time TIME  time of peried between check.
  -vvv, --verbose       dump all log.
```

```python
#/bin/python3
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
    wt.do_wait()

```

## 3. Develop

```bash
git clone https://github.com/lijunjie2232/gpu_waiter.git
cd gpu_waiter
pip install -e .
```
---
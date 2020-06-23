# MutiTask
Provideing a component for user to solve problem together on multiple machines quickly.

Multitask provide a component for user to solve problem together on multiple machines quickly.
It finish by redis and thread.
User can finish Distributed deployment just make a tasks generator and task solution.
It also provide api to check status for each device.
And It can receive and save error task until user reload it. 

![](https://github.com/Yakuho/picture/blob/master/t.png)


How to use
----------
For server:
    
For example: I want to solve the problem of website request, so I create a task about creating URL.

**Initialization**: 
- WorksNumb: Device number. Here I set five, it that mean five device will finish this tasks 
together, and device ID would be the Device0, Device1, etc...
- TasksChannelMax： In the tasks channel, the max number of tasks. Here I set to 20.
- InstructionChannelNumb: The number of tasks. Here, I just make the only one task, and 
the task will be put in TaskChannel0. if user create task0(), task1(), task2(), 
InstructionChannelNumb should be set 3, and each task willput in TaskChannel0, TaskChannel1,
TaskChannel2.

the last step is start it.

**After starting, What can user do?**

Command:
 - detect_all: detect all device status. (device mean work node)
 - detect_one: detect the one device status.
 - pause_all：pause all mission of all device.
 - pause_one：pause the one mission of all device.
 - start_all: start all mission of all device.
 - start_one: start the one mission of all device.
 - pause_allot: pause allot task from server.
 - start_allot: start allot task from server.
 - detect_fail_channel: detect the number of fail task in the channel.
 - reload_all_fail_tasks: reload all fail task to task channel.
 - reload_one_fail_task: reload the one fail task to task channel.
 - reset_max_task: reset the max number of task channel can hold.
 - exit、stop、quit: stop all device and close server.

(see doc from Server._ _ init _ _ )

```python
from Mutitask.server import Server


def task():
    for i in range(1, 100):
        yield f'https://www.kuaidaili.com/free/inha/{i}/'


manager = Server(WorksNumb=5, TasksChannelMax=20, InstructionChannelNumb=1)
tasks = [task()]
manager.start(tasks)
```

For Client:

Due to server allot the only task that device must solve it.So I create a function to do that.

**Initialization**:
- device: Client(device) is define device ID, so server can be detect this device status. Here
I just set only device.
- task_func: A function that how deal with the task. Here I create a function for requesting URL 
and get that status.
- save_func: A function that how save the result. Here I just print the result. User also can 
save it in database.

the last step is start it, but It is important that user should define which TaskChannel device
would be get. Due to I just create the only one task of requesting URL, so task must be put in 
the TaskChannel0.

```python
from Mutitask.client import Client
from requests import get


def task_function(task):
    url = task
    response = get(url)
    if response.status_code == 200:
        return response.status_code
    else:
        return None


def save_function(result):
    print(result)


a = Client(device=0)
a.initial_task_function(task_func=task_function)
a.initial_save_function(save_func=save_function)
a.start(channel=0)
```

How define Tasks、TaskFunction and SaveFunction
-----------------------------------------------

- Tasks: 

1. The type of tasks must be generator or iterator.

For example:
  
```python
task = (i for i in range(10))


def task():
    for i in range(10):
        yield f'https://www.****/index{i}/'
```

- TaskFunction:

1. **The receive parameter can only be one.**

2. TaskFunction return must between **result** or **None**.

result mean that success to deal with the task and product data.

None mean that fail to deal with the task and retry 3 times automatically, if both fail in 3 times 
the task will put in FailChannel.

- SaveFunction:
1. The receive parameter can only be one

No other requirements

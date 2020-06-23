# MutiTask
Provideing a component for user to solve problem together on multiple machines quickly.

Multitask provide a component for user to solve problem together on multiple machines quickly.
It finish by redis and thread.
User can finish Distributed deployment just make a tasks generator and task solution.
It also provide api to check status for each device.
And It can receive and save error task until user reload it. 

requirements:
redis, thread.

![](https://github.com/Yakuho/picture/blob/master/t.png)


How to use
----------
For server:
    
For example: I want to solve the problem of website request, so I create a task about creating URL.

**Initialization params**: 
- WorksNumb: Device number. Here I set five, it that mean five device will finish this tasks 
together, and device ID would be the Device1, Device2, etc...
- ChannelSize： In the tasks channel, the max number of tasks. default 50.
- MonitorWait: What time the monitor would wait When detect the device status.
- host: redis server host. default 127.0.0.1
- port: redis server port. default 6379
- db: redis server db. default 0
- password: redis server password. default None

**After starting, What can user do?**

Command:
 - detect_all: detect all device status. (device mean work node)
 - detect_one: detect the one device status.
 - add_device: create a work device at last.
 - del_device: delete a work device from last.
 - pause_all：pause all mission of all device.
 - pause_one：pause the one mission of all device.
 - stop_all: let all device status is off-line.
 - stop_one: let the device status is off-line.
 - start_all: start all mission of all device.
 - start_one: start the one mission of all device.
 - reset_max_task: reset the max number of task channel can hold.
 - detect_fail_task_channel: detect the number of fail task in fail channel
 - reload_all_fail_channel: reload all task from all fail channel to their task channel.
 - reload_one_fail_channel_all_task: reload all task in the one fail channel.
 - reload_one_fail_channel_one_task: reload one task in the one fail channel.
 - del_one_task_by_fail_channel: delete a task from the channel.
 - pause_allot: pause allot task from server.
 - start_allot: start allot task from server.
 - stop_allot: Close allotting mission and stop all device.
 - stop: stop all device and close server.

(see doc from Server)

```python
from Mutitask.server import BaseConfig
from Mutitask.server import Terminal


def task_generator(t1, t2):
    for i in range(t1, t2):
        yield f'https://kuaidaili/index{i}/'


baseConfig = BaseConfig(deviceNumb=5)
terminal = Terminal(baseConfig=baseConfig)
terminal.run([task_generator(0, 10)])
```

For Client:

Due to server allot the only task that device must solve it.So I create a function to do that.

**Initialization params**:

BaseConfig:
- deviceID: Client(device) is define device ID, so server can be detect this device status
- TaskChannelID: get task by task channel ID
- host: redis server host. default 127.0.0.1
- port: redis server port. default 6379
- db: redis server db. default 0
- password: redis server password. default None

FuncItem:
- baseConfig: object of baseConfig.
- load_task_function: load task function of user define.
- load_save_function: load save function of user define.


```python
from Mutitask.client import BaseConfig
from Mutitask.client import FuncItem
from Mutitask.client import Terminal


def func1(result):
    print(result)


def func2(task):
    if 'https://kuaidaili' not in task:
        # fail task will put in fail task channel
        return None
    else:  
        # success task will put in save function
        return task


base = BaseConfig(deviceID=1, TaskChannelID=1)
funcitem = FuncItem(baseConfig=base)
# funcitem.load_save_function(func1)
funcitem.load_task_function(func2)
terminal = Terminal(baseConfig=base, funcItem=funcitem)
terminal.run()
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

1. **The receive parameter must be only one.**

2. TaskFunction return must between **result** or **None**.

result mean that success to deal with the task and product data.

None mean that fail to deal with the task and the task will put in FailChannel.

- SaveFunction:
1. The receive parameter must be only one.

No other requirements

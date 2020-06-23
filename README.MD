# MutiTask
Provideing a component for user to solve problem together on multiple machines quickly.

Multitask provide a component for user to solve problem together on multiple machines quickly.
It finish by redis and thread.
User can finish Distributed deployment just make a tasks generator and task solution.
It also provide api to check status for each device.
And It can receive and save error task until user reload it. 

pip requirements:
redis, thread.

![](https://github.com/Yakuho/picture/blob/master/t.png)

The following example are base on the latest version.

Server
------
Example 1:  
    For spider.Due to request url to get data it need to wait some time fro response, 
    if request one by one, it is inefficient. You can do that.
```python
from Mutitask.server import BaseConfig
from Mutitask.server import Terminal


def task_generator(ps, pe):
    # initial task: get url response text.
    for i in range(ps, pe + 1):
        yield f'https://www.kuaidaili.com/free/inha/{i}/'


if __name__ == '__main__':
    # initial 5 device to finish it, other params set default.
    baseConfig = BaseConfig(deviceNumb=5)
    # get terminal by baseConfig
    terminal = Terminal(baseConfig=baseConfig)
    # posting task get url from 1 to 200
    terminal.run([task_generator(1, 200)])
```

Example 2:  
For calculate. Convolve an image often cost 1 second or more, if you want to convolve 
many image and want to be more efficient. You can do that.
```python
from Mutitask.server import BaseConfig
from Mutitask.server import Terminal
from PIL import Image
from numpy import array


def task_generator(name_s, name_e):
    # initial task: get image matrix to get image after convolution.
    for i in range(name_s, name_e + 1):
        img = Image.open(f'D:/Machine_learning/decode/{i}.jpg').convert('L')
        yield array(img)


if __name__ == '__main__':
    # initial 5 device to finish it, other params set default.
    baseConfig = BaseConfig(deviceNumb=5)
    # get terminal by baseConfig
    terminal = Terminal(baseConfig=baseConfig)
    # posting task get 1 - 200 image matrix, due to send the only 
    # one task mission, task will put in TaskChannel1
    terminal.run(task_generator(1, 200))
```

Client
------
**Corresponding example 1:**

device 1:
```python
from Mutitask.client import BaseConfig
from Mutitask.client import FuncItem
from Mutitask.client import Terminal
from requests import get


def func1(result):
    print(result)


def func2(task):
    headers = {
    'User-Agent': '******************'
    }
    response = get(url=task, headers=headers)
    if response.status_code == 200:
        # success: send result to save function
        return response.text
    else:
        # error: send fail task to FailChannel automatically
        return None


if __name__ == '__main__':
    # initial this device is ID = 1, get task from TaskChannel1
    base = BaseConfig(deviceID=1, TaskChannelID=1)
    # get function item by base.
    funcitem = FuncItem(baseConfig=base)
    # load save function
    funcitem.load_save_function(func1)
    # load request function
    funcitem.load_task_function(func2)
    # get terminal object and use user define save function, 
    # get more about default function please read Mutitask README.md
    terminal = Terminal(baseConfig=base, funcItem=funcitem)
    terminal.run()
```

device 2:
```python
from Mutitask.client import BaseConfig
from Mutitask.client import FuncItem
from Mutitask.client import Terminal
from requests import get


def func1(result):
    print(result)


def func2(task):
    headers = {
    'User-Agent': '******************'
    }
    response = get(url=task, headers=headers)
    if response.status_code == 200:
        # success: send result to save function
        return response.text
    else:
        # error: send fail task to FailChannel automatically
        return None


if __name__ == '__main__':
    # initial this device is ID = 1, get task from TaskChannel1
    base = BaseConfig(deviceID=2, TaskChannelID=1)
    # get function item by base.
    funcitem = FuncItem(baseConfig=base)
    # load save function
    funcitem.load_save_function(func1)
    # load request function
    funcitem.load_task_function(func2)
    # get terminal object and use user define save function, 
    # get more about default function please read Mutitask README.md
    terminal = Terminal(baseConfig=base, funcItem=funcitem)
    terminal.run()
```

device 3 ...

device 4 ...

**Corresponding example 2:**

device 1:
```python
from Mutitask.client import BaseConfig
from Mutitask.client import FuncItem
from Mutitask.client import Terminal
from scipy.signal import convolve2d
from numpy import array


def func2(task):
    # due to task is string, get matrix can after eval()
    img = eval(task)
    kernel = [[-1, 1, -1], 
              [1, -1, 1], 
              [-1, 1, -1]]
    return convolve2d(img, array(kernel), mode='same')


if __name__ == '__main__':
    # initial this device is ID = 1, get task from TaskChannel1
    base = BaseConfig(deviceID=1, TaskChannelID=1)
    # get function item by base.
    funcitem = FuncItem(baseConfig=base)
    # load convolution function
    funcitem.load_task_function(func2)
    # get terminal object and use default save function, 
    # get more about default function please read README.md
    terminal = Terminal(baseConfig=base, funcItem=funcitem)
    terminal.run()
```

device 2:
```python
from Mutitask.client import BaseConfig
from Mutitask.client import FuncItem
from Mutitask.client import Terminal
from scipy.signal import convolve2d
from numpy import array


def func2(task):
    # due to task is string, get matrix can after eval()
    img = eval(task)
    kernel = [[-1, 1, -1], 
              [1, -1, 1], 
              [-1, 1, -1]]
    return convolve2d(img, array(kernel), mode='same')


if __name__ == '__main__':
    # initial this device is ID = 1, get task from TaskChannel1
    base = BaseConfig(deviceID=2, TaskChannelID=1)
    # get function item by base.
    funcitem = FuncItem(baseConfig=base)
    # load convolution function
    funcitem.load_task_function(func2)
    # get terminal object and use default save function, 
    # get more about default function please read README.md
    terminal = Terminal(baseConfig=base, funcItem=funcitem)
    terminal.run()
```
device 3 ...

device 4 ...

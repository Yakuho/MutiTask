from Mutitask.client import BaseConfig
from Mutitask.client import FuncItem
from Mutitask.client import Terminal


def func1(result):
    print(result)


def func2(task):
    return task


if __name__ == '__main__':
    base = BaseConfig(deviceID=1, TaskChannelID=1)
    funcitem = FuncItem(baseConfig=base)
    # funcitem.load_save_function(func1)
    funcitem.load_task_function(func2)
    terminal = Terminal(baseConfig=base, funcItem=funcitem)
    terminal.run()

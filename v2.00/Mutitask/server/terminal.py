from collections.abc import Generator, Iterator
from types import FunctionType
from threading import Thread
from .middleware import RedisAPI
from .control import Control


def CheckTask(tasks):
    """
    if tasks not generator or iterator, raise Error; else return task list.
    """
    if isinstance(tasks, FunctionType) or isinstance(tasks, Generator) or isinstance(tasks, Iterator):
        tasks = [tasks]
    elif isinstance(tasks, list):
        pass
    else:
        raise Exception('tasks maybe error')
    return tasks


class Terminal:
    def __init__(self, baseConfig):
        """
        Initial base config and get api
        :param baseConfig:
        """
        self.base = baseConfig
        self.middleAPI = RedisAPI(self.base)
        self.control = Control(apiConfig=self.middleAPI, baseConfig=self.base)

    def run(self, tasks):
        tasks = CheckTask(tasks=tasks)
        self.base.TaskChannelNumb = len(tasks)
        self.middleAPI.initial_device()
        ControlThread = Thread(target=self.base.ControlStart, args=(self.control.api, ))
        TaskThreadList = [Thread(target=self.base.AllotStart, args=(self.middleAPI.AllotMission, tasks[i], i+1, ))
                          for i in range(self.base.TaskChannelNumb)]
        [taskThread.start() for taskThread in TaskThreadList]
        ControlThread.start()
        [taskThread.join() for taskThread in TaskThreadList]
        ControlThread.join()
        self.middleAPI.close()

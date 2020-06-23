from types import FunctionType
from .middleware import RedisAPI
from time import sleep


class FuncItem:
    def __init__(self, baseConfig):
        self.base = baseConfig
        self.redis = RedisAPI(baseConfig=baseConfig)
        self.__TaskFunc = None
        self.__SaveFunc = self.redis.BuiltinSaveFunc

    def load_task_function(self, func):
        """
        load task function plugin
        """
        if not isinstance(func, FunctionType):
            raise Exception('TaskFunc not a function.')
        self.__TaskFunc = func

    def load_save_function(self, func):
        """
        load task function plugin
        """
        if not isinstance(func, FunctionType):
            raise Exception('SaveFunc not a function.')
        self.__SaveFunc = func

    def ExecuteMission(self):
        if not isinstance(self.__TaskFunc, FunctionType):
            self.base.StopTaskDetecting()
            print('TaskFunc not initial!!!')
        while not self.base.TaskMissionStop:
            while not self.base.TaskMissionPause:
                task = self.redis.get_task()
                if task:
                    result = self.__TaskFunc(task)
                    if result:
                        self.__SaveFunc(result)
                    else:
                        self.redis.roll_task(task)
                sleep(self.base.NormalReactTime)
            sleep(self.base.PauseReactTime)

    def ExecuteDetect(self):
        """
        Detect current device state, adjust action if it chance
        :return:
        """
        LastStatue = self.redis.detect_self()
        while not self.base.DetectStop:
            state = self.redis.detect_self()
            try:
                LastStatue = int(LastStatue)
                state = int(state)
            except TypeError:
                self.base.StopTaskDetecting()
                break
            if LastStatue != state:
                if state is self.base.DeviceTest:
                    self.redis.update_self(LastStatue)
                elif state is self.base.DevicePause:
                    LastStatue = state
                    self.base.PauseTaskMission()
                elif state is self.base.DeviceStart:
                    self.base.StartTaskMission()
                    LastStatue = state
                elif state is self.base.DeviceOffLine:
                    self.base.StopTaskMission()
            sleep(self.base.PauseReactTime)
        print(f'device{self.base.DeviceID} has been stopped.')

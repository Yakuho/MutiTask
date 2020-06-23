from .setting import *
from time import sleep


class BaseConfig:
    """
    # ======default setting=======
    # redis setting           # ==
    # host = '127.0.0.1'      # ==
    # port = 6379             # ==
    # db = 0                  # ==
    # password = None         # ==
    # ======================================
    # What time the monitor would wait  # ==
    # When detect the device status     # ==
    # MonitorWait = 5                   # ==
    # ==================================================
    # The max number of task in the all TaskChannel # ==
    # TaskChannelMax = 50                           # ==
    # ==================================================
    """
    def __init__(self, deviceNumb, host=Host, port=Port, db=Db, password=Password,
                 ChannelSize=TaskChannelMax, MonitorWaitTime=MonitorWait):
        # ==================================
        # react time setting            # ==
        self.NormalReactTime = 0.05     # ==
        self.PauseReactTime = 0.1       # ==
        # ==================================
        # Allotting mission status      # ==
        self.__TaskAllotPause = False   # ==
        self.__TaskAllotStop = False    # ==
        # ==================================
        # Controlling system status     # ==
        self.__ControlStop = False      # ==
        # ==================================
        # Redis setting                 # ==
        self.host = host                # ==
        self.port = port                # ==
        self.db = db                    # ==
        self.password = password        # ==
        # ======================================
        # device status setting             # ==
        self.DevicePause = DevicePause      # ==
        self.DeviceStart = DeviceStart      # ==
        self.DeviceOffLine = DeviceOffLine  # ==
        self.DeviceTest = DeviceTest        # ==
        # ==================================================
        # Channel setting                               # ==
        # How many task would you set                   # ==
        self.TaskChannelNumb = TaskChannelNumb          # ==
        # The max number of task in the TaskChannel     # ==
        self.TaskChannelMax = ChannelSize               # ==
        # ==================================================
        # Device setting                                # ==
        # The name of key about device status           # ==
        self.DeviceKeyName = DeviceKeyName              # ==
        # The number of device                          # ==
        self.DeviceNumb = deviceNumb                    # ==
        # What time the monitor would wait When detect  # ==
        # the device status                             # ==
        self.MonitorWait = MonitorWaitTime              # ==
        # ==================================================
        # pipeline name setting                         # ==
        # the name of fail task channel                 # ==
        self.FailChannelHost = FailChannelHost          # ==
        # the name of task channel                      # ==
        self.TaskChannelHost = TaskChannelHost          # ==
        # built-in save channel                         # ==
        self.SaveBuiltinHost = SaveBuiltinHost          # ==
        # ==================================================

    # 暂停任务分发
    def PauseTaskAllot(self, *args, **kwargs):
        """
        Pause allotting mission.
        :return:
        """
        self.__TaskAllotPause = True
        return 'has been pause task allotting'

    # 开启任务分发
    def StartTaskAllot(self, *args, **kwargs):
        """
        Start allotting mission.
        :return:
        """
        self.__TaskAllotPause = False
        return 'has been start task allotting'

    # 关闭任务分发并停止输入
    def StopTaskSystem(self, *args, **kwargs):
        """
        Close allotting mission and stop all device.
        :return:
        """
        self.__TaskAllotPause = True
        self.__TaskAllotStop = True
        self.__ControlStop = True
        return 'has been stop task allotting and stop all device.'

    # 关闭任务分发
    def StopTaskAllot(self, *args, **kwargs):
        """
        Close allotting mission and stop all device.
        :return:
        """
        self.__TaskAllotPause = True
        self.__TaskAllotStop = True
        return 'has been stop task allotting and stop all device.'

    # 运行分发函数
    def AllotStart(self, func, *args, **kwargs):
        """
        execute Allotting function.
        :param func: FunctionType
        :return:
        """
        args, kwargs = args, kwargs
        while not self.__TaskAllotStop:
            while not self.__TaskAllotPause:
                func(*args, **kwargs)
                sleep(self.NormalReactTime)
            sleep(self.PauseReactTime)

    # 控制运行函数
    def ControlStart(self, func, *args, **kwargs):
        """
        execute Control function.
        :param func: iterator or generator
        :return:
        """
        args, kwargs = args, kwargs
        while not self.__ControlStop:
            func(*args, **kwargs)
            sleep(self.PauseReactTime)

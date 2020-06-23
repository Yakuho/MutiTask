from .setting import *


class BaseConfig:
    """
    # ======default setting=======
    # redis setting           # ==
    # host = '127.0.0.1'      # ==
    # port = 6379             # ==
    # db = 0                  # ==
    # password = None         # ==
    # ============================
    """
    def __init__(self, deviceID, TaskChannelID, host=Host, port=Port, db=Db, password=Password):
        # ==================================
        # react time setting            # ==
        self.NormalReactTime = 0.05     # ==
        self.PauseReactTime = 0.1       # ==
        # ==================================
        # Execute mission status        # ==
        self.TaskMissionPause = True    # ==
        self.TaskMissionStop = False    # ==
        # ==================================
        # Controlling system status     # ==
        self.DetectStop = False         # ==
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
        # Device setting                                # ==
        # The name of key about device status           # ==
        self.DeviceKeyName = DeviceKeyName              # ==
        # The ID of device                              # ==
        self.DeviceID = deviceID                        # ==
        # the task channel ID                           # ==
        self.TaskChannelID = TaskChannelID              # ==
        # ==================================================
        # pipeline name setting                         # ==
        # the name of fail task channel                 # ==
        self.FailChannelHost = FailChannelHost          # ==
        # the name of task channel                      # ==
        self.TaskChannelHost = TaskChannelHost          # ==
        # the name of device                            # ==
        self.DeviceHost = DeviceHost                    # ==
        # built-in save channel                         # ==
        self.SaveBuiltinHost = SaveBuiltinHost          # ==
        # ==================================================

    # 暂停做任务
    def PauseTaskMission(self, *args, **kwargs):
        """
        Pause allotting mission.
        :return:
        """
        self.TaskMissionPause = True
        return 'has been pause task allotting'

    # 开启做任务
    def StartTaskMission(self, *args, **kwargs):
        """
        Start execute task function.
        :return:
        """
        self.TaskMissionPause = False
        return 'has been start task allotting'

    # 关闭设备
    def StopTaskDetecting(self, *args, **kwargs):
        """
        Close device.
        :return:
        """
        self.TaskMissionPause = True
        self.TaskMissionStop = True
        self.DetectStop = True
        return 'has been stop task allotting and stop all device.'

    # 关闭做任务
    def StopTaskMission(self, *args, **kwargs):
        """
        Stop execute task function.
        :return:
        """
        self.TaskMissionPause = True
        self.TaskMissionStop = True
        return 'has been stop task allotting and stop all device.'

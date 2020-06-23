# ==========================
# redis setting         # ==
Host = '127.0.0.1'      # ==
Port = 6379             # ==
Db = 0                  # ==
Password = None         # ==
# ==========================
# Root name of task channel
TaskChannelHost = 'TaskChannel'
# Root name of fail task channel
FailChannelHost = 'FailChannel'
# Root name of result channel
SaveBuiltinHost = 'ResultChannel'
# The name of key about device status
DeviceKeyName = 'DeviceTable'
# What time the monitor would wait When detect the device status
MonitorWait = 5
# How many task would you set
TaskChannelNumb = 1
# The max number of task in all TaskChannel
TaskChannelMax = 50
# ========================
# device status       # ==
DevicePause = 0       # ==
DeviceStart = 1       # ==
DeviceOffLine = -1    # ==
DeviceTest = -99      # ==
# ========================

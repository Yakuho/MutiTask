from .terminal import CheckTask
from .terminal import Terminal
from .base import BaseConfig


class UseGuide:
    """
    from Mutitask.server import BaseConfig
    from Mutitask.server import Terminal


    baseConfig = BaseConfig(deviceNumb=5)       # config base attribute such the number of device.
    doc = baseConfig.__doc__                    # read all parameter implication.
    terminal = Terminal(baseConfig=baseConfig)  # get the object of allotting terminal by baseConfig.
    terminal.run(tasks)                         # send tasks and run it.


    # ======================================================================++
    # Example 1:                                                            ||
    #   tasks = (f'https://testurl/index{i}/' for i in range(10))           ||
    #                                                                       ||
    # if tasks is a generator or iterator, redis channel would be:          ||
    #   DeviceTable                                                         ||
    #       ├─ device1                                                      ||
    #       ├─ device2                                                      ||
    #       ├─ device3                                                      ||
    #       ├─ device4                                                      ||
    #       └─ device5                                                      ||
    #   TaskChannel1                                                        ||
    #       ├─ 'https://testurl/index0/'      task 1                        ||
    #       ..............                                                  ||
    #       ├─ 'https://testurl/index8/'      task 9                        ||
    #       ├─ 'https://testurl/index9/'      task 10                       ||
    #   FailChannel1    (if not exist, mean all task is normal)             ||
    #       ├─ ”*********“      fail task 1                                 ||
    #       ..............                                                  ||
    #       ├─ ”*********“      fail task n                                 ||
    #       ├─ ”*********“      fail task n+1                               ||
    # ======================================================================++
    # Example 2:                                                            ||
    #   task1 = (f'https://testurl/index{i}/' for i in range(10))           ||
    #   task2 = (f'https://testurl/index{i}/' for i in range(10, 20))       ||
    #   tasks = [task1, task2]                                              ||
    # if tasks is a list, redis channel would be:                           ||
    #   DeviceTable                                                         ||
    #       ├─ device1                                                      ||
    #       ├─ device2                                                      ||
    #       ├─ device3                                                      ||
    #       ├─ device4                                                      ||
    #       └─ device5                                                      ||
    #   TaskChannel1                                                        ||
    #       ├─ 'https://testurl/index0/'      task 1                        ||
    #       ..............                                                  ||
    #       ├─ 'https://testurl/index8/'      task 9                        ||
    #       ├─ 'https://testurl/index9/'      task 10                       ||
    #   FailChannel1    (if not exist, mean all task is normal)             ||
    #       ├─ ”*********“      fail task 1                                 ||
    #       ..............                                                  ||
    #       ├─ ”*********“      fail task n                                 ||
    #       ├─ ”*********“      fail task n+1                               ||
    #   TaskChannel2                                                        ||
    #       ├─ 'https://testurl/index10/'      task 1                       ||
    #       ..............                                                  ||
    #       ├─ 'https://testurl/index18/'      task 9                       ||
    #       ├─ 'https://testurl/index19/'      task 10                      ||
    #   FailChannel2    (if not exist, mean all task is normal)             ||
    #       ├─ ”*********“      fail task 1                                 ||
    #       ..............                                                  ||
    #       ├─ ”*********“      fail task n                                 ||
    #       ├─ ”*********“      fail task n+1                               ||
    # ======================================================================++
    """


class CommandGuide:
    def detect_all(self):
        """
        detect all work node
        For example:
            detect_all          mean get status from all device
        :return: {device*: statue, ...}
        """

    def detect_one(self, device):
        """
        detect the one work node by device
        For example:
            detect_one 1          mean get status from the device1
            detect_one 2          mean get status from the device2
            detect_one 3          mean get status from the device3
        :param device:  device id
        :return: {device*: statue}
        """

    # 增加一个工作设备
    def add_device(self, *args, **kwargs):
        """
        create a work device at last.
        For example:
            add_device          such as the number of device is 5, so number increase to 6
        :return:
        """

    # 删除一个工作设备
    def del_device(self, *args, **kwargs):
        """
        delete a work device from last.
        For example:
            del_device          such as the number of device is 6, so number decrease to 5
        :return:
        """

    def pause_all(self):
        """
        pause all work node, but allotting task still continue
        For example:
            pause_all           mean pause all device mission
        :return:
        """

    def pause_one(self, device):
        """
        pause the one work node by device, but other work node and allotting task still continue
        For example:
            pause_one 0          mean get pause the device0 mission
            pause_one 1          mean get pause the device1 mission
            pause_one 2          mean get pause the device2 mission
        :param device: device id
        :return:
        """

    def stop_all(self):
        """
        let all device status is off-line.
        For example:
            stop_all        mean that device* is off-line
        :return:
        """

    def stop_one(self):
        """
        let the device status is off-line.
        For example:
            stop_one 1       mean that device1 is off-line
            stop_one 2       mean that device3 is off-line
            stop_one 3       mean that device3 is off-line
        :return:
        """

    def start_all(self):
        """
        start all work node, due to work node in pause state originally
        For example:
            start_all         mean start device mission.
        :return:
        """

    def start_one(self, device):
        """
        start the one work node, work node in pause state originally
        For example:
            start_one 0         mean start device0 mission.
            start_one 1         mean start device1 mission.
            start_one 2         mean start device2 mission.
        :param device:
        :return:
        """

    def reset_task_max(self, number):
        """
        reset task's pipeline max capacity
        For example:
            reset_task_max 50           mean reset max TaskChanel can holding
        :param number:  capacity number
        :return:
        """

    # 探测某一失败任务通道的任务数量
    def detect_fail_task_channel(self, channel, *args, **kwargs):
        """
        detect the number of fail task in fail channel
        For example:
            detect_fail_task_channel 1          mean detect the number of fail task in FailChannel1
            detect_fail_task_channel 2          mean detect the number of fail task in FailChannel2
            detect_fail_task_channel 3          mean detect the number of fail task in FailChannel3
        :return:
        """

    # 重载所有的失败通道任务至对应的任务通道
    def reload_all_fail_channel(self, *arg, **kwargs):
        """
        reload all task from all fail channel to their task channel.
        For example:
            reload_all_fail_channel             mean reload all task to each TaskChannel from all FailChannel
        :return:
        """

    # 重载某一失败通道所有任务至对应的任务通道
    def reload_one_fail_channel_all_task(self, channel, *args, **kwargs):
        """
        reload all task in the one fail channel
        For example:
            reload_one_fail_channel_all_task 1      mean reload all task to TaskChannel1 from FailChannel1
            reload_one_fail_channel_all_task 2      mean reload all task to TaskChannel2 from FailChannel2
            reload_one_fail_channel_all_task 3      mean reload all task to TaskChannel3 from FailChannel3
        :param channel:
        :return:
        """

    # 重载某一失败通道非所有任务至对应的任务通道
    def reload_one_fail_channel_one_task(self, channel, task_id, *args, **kwargs):
        """
        reload one task in the one fail channel
        For example:
            reload_one_fail_channel_one_task 1 3        mean reload task3 to TaskChannel1 from FailChannel1
            reload_one_fail_channel_one_task 1 5        mean reload task5 to TaskChannel1 from FailChannel1
            reload_one_fail_channel_one_task 2 3        mean reload task3 to TaskChannel2 from FailChannel2
            reload_one_fail_channel_one_task 5 1        mean reload task1 to TaskChannel5 from FailChannel5
        :param channel:  fail channel id
        :param task_id:  fail task id
        :return:
        """

    # 删除某一失败队列中的某个任务
    def del_one_task_by_fail_channel(self, channel, task_id, *args, **kwargs):
        """
        delete a task from the channel.
        For example:
            del_one_task_by_fail_channel 1 3        mean delete task3 from FailChannel1
            del_one_task_by_fail_channel 1 6        mean delete task6 from FailChannel1
            del_one_task_by_fail_channel 2 3        mean delete task3 from FailChannel2
            del_one_task_by_fail_channel 5 3        mean delete task3 from FailChannel5
        :param channel:  fail channel id
        :param task_id:  fail task id
        :return:
        """

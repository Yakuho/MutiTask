from collections.abc import Iterator, Generator
from redis import ConnectionPool, StrictRedis
from time import sleep


class RedisAPI:
    """
    API base on redis.
    """
    def __init__(self, baseConfig):
        self.base = baseConfig
        self.redis = StrictRedis(
            connection_pool=ConnectionPool(host=self.base.host, port=self.base.port, db=self.base.db,
                                           password=self.base.password, decode_responses=True))

    # 删除临时键和关闭redis服务
    def close(self):
        """
        delete keys and close redis server.
        :return:
        """
        for item in self.redis.keys():
            for i in [self.base.TaskChannelHost, self.base.FailChannelHost, self.base.SaveBuiltinHost]:
                if i in item:
                    break
            else:
                self.redis.delete(item)
        else:
            self.redis.close()
            return 'success close redis.'

    # 初始化 创建key： DeviceTable 并设置全部设备为0： 暂停状态
    def initial_device(self):
        """
        Initial all device status.
        :return:
        """
        for item in range(1, self.base.DeviceNumb + 1):
            self.redis.hset(name=self.base.DeviceKeyName, key=f'device{item}', value=0)
        else:
            return 'success initial all device.'

    # 探测所有工作设备的状态
    def detect_all(self, *args, **kwargs):
        """
        detect all device
        :return: state of all device
        """
        for item in self.redis.hgetall(name=self.base.DeviceKeyName):
            self.redis.hset(name=self.base.DeviceKeyName, key=item, value=self.base.DeviceTest)
        else:
            sleep(self.base.MonitorWait)
        return self.redis.hgetall(name=self.base.DeviceKeyName)

    # 探测某一个工作设备的状态
    def detect_one(self, device, *args, **kwargs):
        """
        detect one device, return one device state
        :param device: 节点号
        :return: state of the device
        """
        if f'device{device}' not in self.redis.hgetall(name=self.base.DeviceKeyName):
            return f'error! not exist device{device}'
        self.redis.hset(name=self.base.DeviceKeyName, key=f'device{device}', value=self.base.DeviceTest)
        sleep(self.base.MonitorWait)
        return {f'device{device}': self.redis.hget(self.base.DeviceKeyName, f'device{device}')}

    # 增加一个工作设备
    def add_device(self, *args, **kwargs):
        """
        create a work device
        :return:
        """
        self.base.DeviceNumb += 1
        self.redis.hset(name=self.base.DeviceKeyName, key=f'device{self.base.DeviceNumb}', value=self.base.DevicePause)
        return 'success add a new device.'

    # 删除一个工作设备
    def del_device(self, *args, **kwargs):
        """
        delete a work device
        :return:
        """
        if self.redis.hlen(name=self.base.DeviceKeyName) <= 0:
            return 'DeviceTable have no device.'
        self.redis.hget(name=self.base.DeviceKeyName, key=f'device{self.base.DeviceNumb}')
        self.base.DeviceNumb -= 1
        return 'success delete a device.'

    # 暂停所有工作设备
    def pause_all(self, *args, **kwargs):
        """
        pause all work node
        :return:
        """
        for item in self.redis.hgetall(name=self.base.DeviceKeyName):
            self.redis.hset(name=self.base.DeviceKeyName, key=item, value=self.base.DevicePause)
        else:
            return 'success pause all device.'

    # 暂停某一个工作设备
    def pause_one(self, device, *args, **kwargs):
        """
        pause one work node
        :param device: device ID
        :return:
        """
        if f'device{device}' not in self.redis.hgetall(name=self.base.DeviceKeyName):
            return f'error! not exist device{device}'
        self.redis.hset(name=self.base.DeviceKeyName, key=f'device{device}', value=self.base.DevicePause)
        return f'success pause device{device}.'

    # 开启所有工作设备
    def start_all(self, *args, **kwargs):
        """
        run all work node
        :return:
        """
        for item in self.redis.hgetall(name=self.base.DeviceKeyName):
            self.redis.hset(name=self.base.DeviceKeyName, key=item, value=self.base.DeviceStart)
        else:
            return 'success start all device.'

    # 开启某一个工作设备
    def start_one(self, device, *args, **kwargs):
        """
        run one work node
        :param device: device ID
        :return:
        """
        if f'device{device}' not in self.redis.hgetall(name=self.base.DeviceKeyName):
            return f'error! not exist device{device}'
        self.redis.hset(name=self.base.DeviceKeyName, key=f'device{device}', value=self.base.DeviceStart)
        return f'success start device{device}.'

    # 离线所有工作设备
    def stop_all(self, *args, **kwargs):
        """
        run all work node
        :return:
        """
        for item in self.redis.hgetall(name=self.base.DeviceKeyName):
            self.redis.hset(name=self.base.DeviceKeyName, key=item, value=self.base.DeviceOffLine)
        else:
            return 'success set all device off-line.'

    # 离线某一个工作设备
    def stop_one(self, device, *args, **kwargs):
        """
        run one work node
        :param device: device ID
        :return:
        """
        if f'device{device}' not in self.redis.hgetall(name=self.base.DeviceKeyName):
            return f'error! not exist device{device}'
        self.redis.hset(name=self.base.DeviceKeyName, key=f'device{device}', value=self.base.DeviceOffLine)
        return f'success set device{device} off-line.'

    # 重置全部任务通道的最大存在数
    def reset_task_max(self, numb, *args, **kwargs):
        """
        reset max tasks channel number
        :param numb: tasks number
        :return:
        """
        try:
            # max size can not negative
            if int(numb) > 0:
                self.base.TaskChannelMax = int(numb)
                return f'success reset task max: {numb}'
            else:
                return 0
        # size must be number, not word
        except ValueError:
            return 0

    # 探测某一失败任务通道的任务数量
    def detect_fail_task_channel(self, channel, *args, **kwargs):
        """
        detect the number of fail task in fail channel
        :return:
        """
        return {f'{self.base.FailChannelHost}{channel}': self.redis.llen(f'{self.base.FailChannelHost}{channel}')}

    # 重载所有的失败通道任务至对应的任务通道
    def reload_all_fail_channel(self, *arg, **kwargs):
        """
        reload all task from all fail channel to their task channel.
        :return:
        """
        for item in self.redis.keys():
            if self.base.FailChannelHost in item:
                number = self.redis.llen(item)
                for i in range(number):
                    task = self.redis.lpop(item)
                    self.redis.rpush(f'{self.base.TaskChannelHost}{item[-1]}', task)
        else:
            return 'has been reload all task from all fail channel'

    # 重载某一失败通道所有任务至对应的任务通道
    def reload_one_fail_channel_all_task(self, channel, *args, **kwargs):
        """
        reload all task in the one fail channel
        :param channel:
        :return:
        """
        try:
            channel = int(channel)
            if channel < 0:
                return 0
        except ValueError:
            return 0
        number = self.redis.llen(f'{self.base.FailChannelHost}{channel}')
        for i in range(number):
            task = self.redis.lpop(f'{self.base.FailChannelHost}{channel}')
            self.redis.rpush(f'{self.base.TaskChannelHost}{channel}', task)
        else:
            return f'has been reload all task from fail channel{channel}'

    # 重载某一失败通道非所有任务至对应的任务通道
    def reload_one_fail_channel_one_task(self, channel, task_id, *args, **kwargs):
        """
        reload one task in the one fail channel
        :param channel:  fail channel id
        :param task_id:  fail task id
        :return:
        """
        try:
            channel = int(channel)
            task_id = int(task_id)
            if channel < 0:
                return 0
        except ValueError:
            return 0
        task = self.redis.lindex(name=f'{self.base.FailChannelHost}{channel}', index=task_id)
        if task:
            self.redis.rpush(f'{self.base.TaskChannelHost}{channel}', task)
        return f'has been reload task{task_id} from fail channel{channel}'

    # 删除某一失败队列中的某个任务
    def del_one_task_by_fail_channel(self, channel, task_id, *args, **kwargs):
        """
        delete a task from the channel.
        :param channel:  fail channel id
        :param task_id:  fail task id
        :return:
        """
        try:
            channel = int(channel)
            task_id = int(task_id)
            if channel < 0:
                return 0
        except ValueError:
            return 0
        self.redis.lindex(name=f'{self.base.FailChannelHost}{channel}', index=task_id)
        return f'has been delete task{task_id} from fail channel{channel}'

    # 任务分发函数
    def AllotMission(self, task, channel):
        """
        Terminal of Allot mission.
        :param task: type of generator or iterator
        :param channel: task channel number
        :return:
        """
        if not isinstance(task, (Iterator, Generator)):
            self.base.StopTaskSystem()
            raise TypeError('tasks must be iterator or generator')
        if self.redis.llen(f'{self.base.TaskChannelHost}{channel}') < self.base.TaskChannelMax:
            try:
                task = next(task)
                self.redis.rpush(f'{self.base.TaskChannelHost}{channel}', task)
            except StopIteration:
                self.base.StopTaskAllot()
                print(f'\nall task has put in task channel{channel}.')

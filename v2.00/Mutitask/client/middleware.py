from redis import ConnectionPool, StrictRedis


class RedisAPI:
    def __init__(self, baseConfig):
        self.base = baseConfig
        self.redis = StrictRedis(
            connection_pool=ConnectionPool(host=self.base.host, port=self.base.port,
                                           db=self.base.db, password=self.base.password, decode_responses=True)
        )

    # 内置保存结果函数
    def BuiltinSaveFunc(self, result):
        """
        built-in save function
        :return:
        """
        self.redis.rpush(f'{self.base.SaveBuiltinHost}{self.base.TaskChannelID}', result)

    # 从对应的任务管道取任务
    def get_task(self):
        """
        Getting task from channel
        :return: task
        """
        return self.redis.lpop(f'{self.base.TaskChannelHost}{self.base.TaskChannelID}')

    # 将失败任务放入失败管道
    def roll_task(self, task):
        """
        Rolling back fail task into FailChannel
        """
        self.redis.rpush(f'{self.base.FailChannelHost}{self.base.TaskChannelID}', task)

    # 更改设备状态
    def update_self(self, status):
        """
        update self status
        """
        self.redis.hset(name=self.base.DeviceKeyName, key=f'{self.base.DeviceHost}{self.base.DeviceID}', value=status)

    # 监测自身设备的状态
    def detect_self(self):
        """
        detect self status
        """
        result = self.redis.hget(name=self.base.DeviceKeyName, key=f'{self.base.DeviceHost}{self.base.DeviceID}')
        if result:
            return int(result)

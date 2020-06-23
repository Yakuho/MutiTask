from redis import ConnectionPool, StrictRedis
from types import FunctionType
from threading import Thread
from time import sleep
DataTempKey = 'Result'
DeviceKey = 'DeviceTable'
FailChannel = 'FailChannel'
TaskChannel = 'TasksChannel'


class Worker:
    """
    Work step:
        work = Worker(device=0)     let this device or thread to be a device0
        work.InitialSolveTaskWay(lambda x: x**2)    define work node ability of solve task
        work.InitialSaveWay()
        work.Run(channel=0)
    Running prepare;
        1. assign this worker ID.
        2. define a function about solving the task.
        3. using default saving function, or define a new saving function.
           default saving function is putting data to channel named Result.
        4. send parameter what task channel ID do you want to solve.
    Define function requirement:
        1. A function about solving the task (Focus):
            Include how to solve and how to handle when meet a error. if return NoneType that
            put it to error channel, else save it.
        2. Saving function:
            It can success to save data.
    """
    def __init__(self, device, host='localhost', port=6379, db=0, password=None):
        self.__MyRedis = StrictRedis(
            connection_pool=ConnectionPool(host=host, port=port, db=db, password=password, decode_responses=True)
        )
        self.__Device = device
        self.__TaskApproach = None
        self.__SaveApproach = None
        self.__StateMaintenanceState = True
        self.__ExecuteTaskStop = False
        self.__ExecuteTaskPause = True

    def __DefaultSave__(self, data):
        """
        Default approach for saving data
        :param data:
        :return:
        """
        self.__MyRedis.rpush(DataTempKey, data)

    def InitialSolveTaskWay(self, task_func):
        """
        Initial approach of solving task.
        :param task_func: way of solve the task
        :return:
        """
        if not isinstance(task_func, FunctionType):
            raise Exception('It is not a function.')
        self.__TaskApproach = task_func

    def InitialSaveWay(self, save_func=None):
        """
        Initial how to save the result after solving task, default save in redis which named Result
        :param save_func:
        :return:
        """
        if save_func:
            self.__SaveApproach = save_func
        else:
            self.__SaveApproach = self.__DefaultSave__

    def GetTask(self, channel):
        """
        Getting task from channel
        :param channel: channel name
        :return: task
        """
        return self.__MyRedis.lpop(channel)

    def StateMaintenance(self):
        """
        Detect current device state, adjust action if it chance
        :return:
        """
        LastStatue = self.__MyRedis.hget(DeviceKey, f'device{self.__Device}')
        while self.__StateMaintenanceState:
            state = self.__MyRedis.hget(DeviceKey, f'device{self.__Device}')
            try:
                LastStatue = int(LastStatue)
                state = int(state)
            except TypeError:
                self.__ExecuteTaskStop = True
                self.__ExecuteTaskPause = True
                return
            if LastStatue != state:
                if state is -1:
                    self.__MyRedis.hset(DeviceKey, f'device{self.__Device}', LastStatue)
                elif state is 0:
                    LastStatue = state
                    self.__ExecuteTaskPause = True
                elif state is 1:
                    self.__ExecuteTaskPause = False
                    LastStatue = state
            sleep(0.1)

    def ExecuteTask(self, channel):
        """
        Getting task to execute from channel, if channel not exist that maybe tasks has been done
        or doesn't exist this channel.  And if get fail mission, it would send to fail channel.
        :param channel: the channel id of getting task
        :return:
        """
        channel = f'{TaskChannel}{channel}'
        if channel not in self.__MyRedis.keys():
            print(f'not exist {channel} or tasks has been done')
            self.__StateMaintenanceState = False
            return None
        while not self.__ExecuteTaskStop:
            while not self.__ExecuteTaskPause:
                task = self.GetTask(channel)
                if task:
                    try:
                        result = self.__TaskApproach(task)
                        if result:
                            self.__SaveApproach(result)
                        else:
                            self.__MyRedis.rpush(f'{FailChannel}{channel}', task)
                    except Exception as e:
                        assert e is None, 'The way for solving task is error.'
                sleep(0.1)
            sleep(0.4)

    def Run(self, ChannelID):
        StateMaintenanceThread = Thread(target=self.StateMaintenance)
        ExecuteTaskThread = Thread(target=self.ExecuteTask, args=(ChannelID, ))
        StateMaintenanceThread.start()
        ExecuteTaskThread.start()
        StateMaintenanceThread.join()
        ExecuteTaskThread.join()
        self.__MyRedis.close()

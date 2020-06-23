from collections.abc import Iterator, Generator
from redis import ConnectionPool, StrictRedis
from threading import Thread
from os.path import abspath
from time import sleep
TasksChannel = 'TasksChannel'   # 任务存放表名
FailChannel = 'FailChannel'  # 任务失败存放点
DeviceKey = 'DeviceTable'   # 节点状态存放表名
MonitorWait = 5     # 监控器等待回响的时间


class Manager:
    """
    工作节点的状态: -1离线   0暂停   1正常
    工作节点应在接受检测前保存上一个状态，在遇到探测信号-1时，应将-1更改为上一状态
    管理节点首先初始化工作节点的数目并将工作节点的状态设为0
    管理节点属性:
                WorksNumb: 管理节点的总数
                InstructionChannelNumb: 任务通道的总数
                TasksChannelMax: 通道最大存在任务数
    管理节点命令:
                MonitorAll向所有工作节点探测当前工作状态
                MonitorOne向指定的工作节点探测当前工作状态
                PauseAll暂停所有工作节点的工作
                PauseOne暂停指定工作节点的工作
                StartAll启动所有工作节点的工作
                StartOne启动指定工作节点的工作
                PauseTasks暂停当前管理节点的任务分发工作
                StartTasks开始当前管理节点的任务分发工作
                reload_all_fail_tasks重载全部失败任务至任务通道
                reload_one_fail_task重载某一失败任务至任务通道
                ResetTaskMax重置任务存在最大数
                exit、stop中止所有工作节点并关闭管理节点
    Example:
        import OracleSpider
        manager = OracleSpider.Manager(WorksNumb=10)    创建10个工作监测节点，默认最大任务存在数=50, 任务分发通道=1
        tasks = (something)->type iterator              创建一个任务分发生成器, 如果是多任务的，就将任务分发通道改为相应的数
        manager = run([tasks])                          将任务生成器放入列表中并开始运行
    D:/>resettaskmax 20 更改最大任务存在数为20
    D:/>startall        启动所有工作节点
    D:/>pauseone 0      暂停0号工作节点
    D:/>startone 0      启动0号工作节点
    D:/>stop            暂停所有工作节点且关闭管理节点(未完成的任务仍会继续存在缓存缓存当中，下次启动时要对应更改分发任务的规则)
    """
    def __init__(self, WorksNumb, host='localhost', port=6379, db=0, password=None,
                 InstructionChannelNumb=1, TasksChannelMax=50):
        self.__MyRedis = StrictRedis(
            connection_pool=ConnectionPool(host=host, port=port, db=db, password=password, decode_responses=True)
        )
        self.WorksNumb = [i for i in range(WorksNumb)]  # 工作节点编号
        self.InstructionChannelNumb = InstructionChannelNumb    # 任务通道数
        self.TasksChannelMax = TasksChannelMax  # 最大存在任务数
        self.__ControlStatue = True
        self.__TaskPause = False
        self.__TaskStop = False

    def InitialMonitor(self, *args, **kwargs):
        """
        initial work node state, work node original state is 0(pause) state
        :return:
        """
        if DeviceKey in self.__MyRedis.keys():
            self.__MyRedis.delete(DeviceKey)
        for item in self.WorksNumb:
            self.__MyRedis.hset(name=DeviceKey, key=f'device{item}', value=0)

    def MonitorAll(self, *args, **kwargs):
        """
        detect all device
        :return: state of all device
        """
        for item in self.WorksNumb:
            self.__MyRedis.hset(name=DeviceKey, key=f'device{item}', value=-1)
        else:
            sleep(MonitorWait)
        return self.__MyRedis.hgetall(DeviceKey)

    def MonitorOne(self, device, *args, **kwargs):
        """
        detect one device, return one device state
        :param device: 节点号
        :return: state of the device
        """
        if f'device{device}' not in self.__MyRedis.hgetall(DeviceKey):
            return f'error! not exist device{device}'
        self.__MyRedis.hset(name=DeviceKey, key=f'device{device}', value=-1)
        sleep(MonitorWait)
        return {f'device{device}': self.__MyRedis.hget(DeviceKey, f'device{device}')}

    def PauseAll(self, *args, **kwargs):
        """
        pause all work node
        :return:
        """
        for item in self.WorksNumb:
            self.__MyRedis.hset(name=DeviceKey, key=f'device{item}', value=0)

    def PauseOne(self, device, *args, **kwargs):
        """
        pause one work node
        :param device: device ID
        :return:
        """
        if f'device{device}' not in self.__MyRedis.hgetall(DeviceKey):
            return 0
        self.__MyRedis.hset(name=DeviceKey, key=f'device{device}', value=0)

    def StartAll(self, *args, **kwargs):
        """
        run all work node
        :return: 
        """
        for item in self.WorksNumb:
            self.__MyRedis.hset(name=DeviceKey, key=f'device{item}', value=1)

    def StartOne(self, device, *args, **kwargs):
        """
        run one work node
        :param device: device ID
        :return:
        """
        if f'device{device}' not in self.__MyRedis.hgetall(DeviceKey):
            return 0
        self.__MyRedis.hset(name=DeviceKey, key=f'device{device}', value=1)

    def ResetTaskMax(self, numb, *args, **kwargs):
        """
        reset max tasks channel number
        :param numb: tasks number
        :return:
        """
        self.TasksChannelMax = int(numb)

    def PauseTasks(self, *args, **kwargs):
        """
        pause allot mission
        :return:
        """
        self.__TaskPause = True

    def StartTasks(self, *args, **kwargs):
        """
        start allot mission
        :return:
        """
        self.__TaskPause = False

    def MonitorFailChannel(self, *args, **kwargs):
        """
        detect the number of fail channel
        :return:
        """
        return {FailChannel: self.__MyRedis.llen(FailChannel)}

    def ReloadAllFailChannel(self, param, *args, **kwargs):
        """
        reload the one fail task to task channel
        :return:
        """
        FChannel, TChannel = param.split(',')
        try:
            TChannel = int(TChannel)
            if TChannel < 0:
                return f'can not reload in {TasksChannel}{TChannel}'
        except ValueError:
            return f'can not reload in {TasksChannel}{TChannel}'
        try:
            FChannel = int(FChannel)
            if FChannel < 0:
                return f'can not reload in {FailChannel}{FChannel}'
        except ValueError:
            return f'can not reload in {FailChannel}{FChannel}'
        number = self.__MyRedis.llen(FailChannel)
        for i in range(number):
            task = self.__MyRedis.lpop(f'{FailChannel}{FChannel}')
            self.__MyRedis.rpush(f'{TasksChannel}{TChannel}', task)
        return 'reload fail task has been done'

    def ReloadOneFailChannel(self, param,  *args, **kwargs):
        """
        reload the one fail task to task channel
        :return:
        """
        FChannel, TChannel, No = param.split(',')
        try:
            TChannel = int(TChannel)
            if TChannel < 0:
                return f'can not reload in {TasksChannel}{TChannel}'
        except ValueError:
            return f'can not reload in {TasksChannel}{TChannel}'
        try:
            FChannel = int(FChannel)
            if FChannel < 0:
                return f'can not reload in {FailChannel}{FChannel}'
        except ValueError:
            return f'can not reload in {FailChannel}{FChannel}'
        try:
            No = int(No)
        except ValueError:
            return f'can not get data of index: {No}'
        task = self.__MyRedis.lindex(f'{FailChannel}{FChannel}', No)
        if task:
            self.__MyRedis.rpush(f'{TasksChannel}{TChannel}', task)
        else:
            return f'can not get data of index: {No}'

    def TasksAllot(self, tasks, channel):
        """
        子线程    通过传入任务，由管理节点分发任务,分发完成关闭Control模块
        :param tasks: iterator or generator
        :param channel: channel ID
        :return:
        """
        if not (isinstance(tasks, Iterator) or isinstance(tasks, Generator)):
            self.__ControlStatue = False
            raise TypeError('tasks must be iterator or generator')
        while not self.__TaskStop:
            while not self.__TaskPause:
                if self.__MyRedis.llen(channel) <= self.TasksChannelMax:
                    try:
                        task = next(tasks)
                        self.__MyRedis.rpush(channel, task)
                    except StopIteration:
                        print('\nallot mission done')
                        return
                sleep(0.1)
            sleep(0.5)

    def Control(self):
        """
        control by keyboard
        :return:
        """
        CommandList = ['detect_all', 'detect_one', 'start_all', 'start_one', 'pause_all', 'pause_one',
                       'pause_allot', 'start_allot', 'reset_task_max', 'detect_fail_channel',
                       'reload_all_fail_tasks', 'reload_one_fail_task']
        ApiList = [self.MonitorAll, self.MonitorOne, self.StartAll, self.StartOne, self.PauseAll, self.PauseOne,
                   self.PauseTasks, self.StartTasks, self.ResetTaskMax, self.MonitorFailChannel,
                   self.ReloadAllFailChannel, self.ReloadOneFailChannel]
        Hash = dict(zip(CommandList, ApiList))
        while self.__ControlStatue:
            sleep(0.4)
            command = input(abspath('').replace('\\', '/') + '>').split(' ')
            command[0] = command[0].lower()
            if command[0] in ['stop', 'exit', 'quit']:
                self.__TaskStop = True
                self.__TaskPause = True
                print('Manager has been stopped')
                break
            if command[0] in Hash:
                try:
                    arg = command[1]
                except IndexError:
                    arg = ''
                ans = Hash[command[0]](arg)
                print(ans) if ans else print(f'success to {command[0]}')
            else:
                print('invalid command.')

    def Run(self, tasks: list, *args, **kwargs):
        """

        :param tasks: a list of tasks
        :return:
        """
        self.InitialMonitor()
        if len(tasks) != self.InstructionChannelNumb:
            self.InstructionChannelNumb = len(tasks)
        WorkThread = [Thread(target=self.TasksAllot, args=(task, f'{TasksChannel}{i}'))
                      for i, task in zip(range(self.InstructionChannelNumb), tasks)]
        CommandThread = Thread(target=self.Control)
        [i.start() for i in WorkThread]
        CommandThread.start()
        [i.join() for i in WorkThread]
        CommandThread.join()
        self.__MyRedis.delete(DeviceKey)
        self.__MyRedis.close()

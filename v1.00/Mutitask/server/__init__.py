from .base import Manager


class Server(Manager):
    """
    ========这是管理节点========
    工作节点的状态: -1离线   0暂停   1正常
    管理节点首先初始化工作节点的数目并将工作节点的状态设为0
    管理节点属性:
                WorksNumb: 管理节点的总数
                InstructionChannelNumb: 任务通道的总数
                TasksChannelMax: 通道最大存在任务数
    管理节点命令:
                detect_all向所有工作节点探测当前工作状态
                detect_one向指定的工作节点探测当前工作状态
                pause_all暂停所有工作节点的工作
                pause_one暂停指定工作节点的工作
                start_all启动所有工作节点的工作
                start_one启动指定工作节点的工作
                pause_allot暂停当前管理节点的任务分发工作
                start_allot开始当前管理节点的任务分发工作
                detect_fail_channel查看失败通道任务数
                reload_all_fail_tasks重载全部失败任务至任务通道
                reload_one_fail_task重载某一失败任务至任务通道
                reset_max_task重置任务存在最大数
                exit、stop、quit中止所有工作节点并关闭管理节点
    Example:
        import server
        manager = server.Server(WorksNumb=10)       创建10个工作节点，默认最大任务存在数=50, 任务分发通道=1
        tasks = (something)->type iterator          创建一个任务分发生成器, 如果是多任务的，就将任务分发通道改为相应的数
        manager = run([tasks])                      将任务生成器放入列表中并开始运行
    D:/>resettaskmax 20 更改最大任务存在数为20
    D:/>startall        启动所有工作节点
    D:/>pauseone 0      暂停0号工作节点
    D:/>startone 0      启动0号工作节点
    D:/>stop            暂停所有工作节点且关闭管理节点(未完成的任务仍会继续存在缓存缓存当中，下次启动时要对应更改分发任务的规则)
    ========It is a manager node========
    device statue:
        -1:off-line、 0:pause、 1:running

    attribution:
        WorksNumb: summation of worker node
        InstructionChannelNumb: the channel number of allotting task
        TasksChannelMax: the max capacity of pipeline of task

    system state chance:
        run -> allotting mission start, task's pipeline was put in task, but all worker node in
               pause state, next step is to start all work node.
        start_all -> running all work node, let all work node execute the task.

    attention: and if you want to chance the state of work node or manager node, please read other
        command (see below)
    """
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
            detect_one 0          mean get status from the device0
            detect_one 1          mean get status from the device1
            detect_one 2          mean get status from the device2
        :param device:  device id
        :return: {device*: statue}
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

    def pause_allot(self):
        """
        pause allot mission, but work node still continue
        For example:
            pause_allot         mean pause server allot mission
        :return:
        """

    def start_allot(self):
        """
        start allot mission
        For example:
            start_allot         mean start server allot mission
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

    def detect_fail_channel(self):
        """
        detect the number of file channel task
        For example:
            detect_fail_channel 0           mean get the number of FailChannel0.
        :return:  {FailChannel: number}
        """

    def reload_all_fail_tasks(self, TaskChannel):
        """
        put all fail tasks into task channel, let those try again
        For example:
            reload_all_fail_tasks 0,0           mean get all fail task from FailChannel0 and put them to TaskChanel0
            reload_all_fail_tasks 0,1           mean get all fail task from FailChannel0 and put them to TaskChanel1
            reload_all_fail_tasks 1,0           mean get all fail task from FailChannel1 and put them to TaskChanel0
        :param TaskChannel: which TaskChannel do you want to reload in
        :return:
        """

    def reload_one_fail_task(self, TaskChannel, ID):
        """
        put the one fail tasks into task channel, let those try again
        For example:
            reload_one_fail_tasks 0,0,0       mean get fail task(index 0) from FailChannel0 and put them to TaskChanel0
            reload_one_fail_tasks 0,0,1       mean get fail task(index 1) from FailChannel0 and put them to TaskChanel0
            reload_one_fail_tasks 0,0,2       mean get fail task(index 2) from FailChannel0 and put them to TaskChanel0
        :param TaskChannel: which TaskChannel do you want to reload in
        :param ID: get fail task from FailChannel index by ID
        :return:
        """

    def stop(self):
        """
        close the manager node and work node
        For example:
            stop            mean stop all device and close server
        :return:
        """

    def quit(self):
        """
        close the manager node and work node
        For example:
            quit            mean stop all device and close server
        :return:
        """

    def start(self, tasks: list):
        """
        start allot mission control terminal
        :param tasks:
        :return:
        """
        self.Run(tasks)

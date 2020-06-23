from .base import Worker


class Client(Worker):
    """
    =======这是工作节点========
    怎么用:
        work = Client(device=0)                       令当前设备为0号设备
        work.initial_task_function(lambda x: x**2)    定义并传入一个解决问题的方法函数
        work.initial_save_function()                  不传入参数，使用默认的保存方案，即临时保存在Result的Redis表
        work.start(channel=0)                         传入参数，意思是从channel0取任务
    运行前准备:
        1. 定义当前的设备id (不能与其他设备重复)
        2. 定义一个解决任务的函数
        3. 定义一个存储结果的函数，或者直接使用默认的函数，即临时保存在Result的Redis表
        4. 传入任务管道的id，意思是从哪个管道取任务
    定义函数的要求:
        1. 解决任务的函数:
            包括如何解决，遇到异常错误如何解决。要求返回只一个值: 若不是None，则存储起来，否则将任务放入失败队列
        2. 存储结果的函数:
            能够成功存储就可

    =======It is worker node=======
    How to use:
        work = Client(device=0)                       let this device or thread to be a device0
        work.initial_task_function(lambda x: x**2)    define work node ability of solve task
        work.initial_save_function()                  no parameter,it is mean using default function to
                                                      save, data will be save in Redis key named Result
        work.start(channel=0)                         It is mean get task from channel0
    Running prepare;
        1. assign this worker ID. (focus: forbid repetition)
        2. define a function about solving the task.
        3. using default saving function, or define a new saving function.
           default saving function is putting data to channel named Result.
        4. send parameter what task channel ID do you want to solve.
    Define function requirement:
        1. A function about solving the task (Focus):
            Include how to solve and how to handle when meet a error. return the only one value,
            if value not NoneType, save it, else put task to fail channel
        2. Saving function:
            It can success to save data.
    """
    def initial_task_function(self, task_func):
        """
        Include how to solve and how to handle when meet a error. if return NoneType that
        put it to error channel, else save it.
        :param task_func:
        :return:
        """
        self.InitialSolveTaskWay(task_func)

    def initial_save_function(self, save_func):
        """
        Include how to save or how to handle data.
        :param save_func:
        :return:
        """
        self.InitialSaveWay(save_func)

    def start(self, channel):
        """
        mission start from channel was send.
        :param channel:
        :return:
        """
        self.Run(channel)

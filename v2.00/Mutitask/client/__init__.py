from .functionitem import FuncItem
from .terminal import Terminal
from .base import BaseConfig


class UseGuide:
    """
    from Mutitask.client import BaseConfig
    from Mutitask.client import FuncItem
    from Mutitask.client import Terminal


    baseConfig = BaseConfig(deviceID=1, TaskChannelID=1)        # config base attribute.
                                                                # this example is that this deviceID is 1,
                                                                # device will get task from TaskChannel1.
    doc = baseConfig.__doc__                    # read all parameter implication.
    funcitem = FuncItem(baseConfig=baseConfig)  # get FuncItem by parameter baseConfig.
    funcitem.load_save_function(func1)          # load save function which user define,
                                                # default result data would put in Result(TaskChannelID)
    funcitem.load_task_function(func2)          # load task function which user define
    terminal = Terminal(baseConfig=baseConfig)  # get the terminal by parameter baseConfig.
    terminal.run()                              # run the device.
    # After running, device was control by server.
    # func1、 func2    defined by user.
    """


class FuncItemAPI:
    """
    Define function requirement:
        1. load_task_function:
            task func:
                1).function param should be only one. (param is task)
                2).function can analysis result by task.
                3).if success to analysis result that must be return result.
                4).else must be return None.
        2. load_save_function:
            save func:
                1).function param should be only one. (param is result)
                2).function can save or handle result.
from .base import BaseConfig
    """
    def __init__(self, baseConfig):
        """
        initial ItemFuncAPI by base config.
        :param baseConfig: base config
        """
        self.baseConfig = baseConfig

    def load_task_function(self, func):
        """
        Include how to solve and how to handle when meet a error. if return NoneType that
        put it to error channel, else save it.
        :param func:
        :return:
        """

    def load_save_function(self, func):
        """
        Include how to save or how to handle data.
        :param func:
        :return:
        """

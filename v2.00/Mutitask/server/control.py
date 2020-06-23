from os.path import abspath


class Control:
    def __init__(self, apiConfig, baseConfig):
        self.middleAPI = apiConfig
        self.base = baseConfig
        self.hashFunc = self.InitialFuncDict()

    # 初始化可执行命令字典
    def InitialFuncDict(self):
        """
        initial middleware api function.
        :return:
        """
        # ==================================================================
        key = ['detect_all', 'detect_one', 'add_device',                # ==
               'del_device', 'pause_all', 'pause_one',                  # ==
               'start_all', 'start_one', 'reset_task_max',              # ==
               'detect_fail_task_channel', 'reload_all_fail_channel',   # ==
               'reload_one_fail_channel_all_task',                      # ==
               'reload_one_fail_channel_one_task',                      # ==
               'del_one_task_by_fail_channel',                          # ==
               'pause_allot', 'start_allot', 'stop_allot', 'stop_all',  # ==
               'stop_one']                                              # ==
        # ==================================================================
        value = [self.middleAPI.detect_all, self.middleAPI.detect_one, self.middleAPI.add_device,
                 self.middleAPI.del_device, self.middleAPI.pause_all, self.middleAPI.pause_one,
                 self.middleAPI.start_all, self.middleAPI.start_one, self.middleAPI.reset_task_max,
                 self.middleAPI.detect_fail_task_channel, self.middleAPI.reload_all_fail_channel,
                 self.middleAPI.reload_one_fail_channel_all_task,
                 self.middleAPI.reload_one_fail_channel_one_task,
                 self.middleAPI.del_one_task_by_fail_channel,
                 self.base.PauseTaskAllot, self.base.StartTaskAllot, self.base.StopTaskAllot,
                 self.middleAPI.stop_all, self.middleAPI.stop_one]
        return dict(zip(key, value))

    def api(self):
        """
        control by input command.
        :return:
        """
        command = input(abspath('').replace('\\', '/') + '>').lower().strip().split(' ')
        func = self.hashFunc.get(command[0])
        if func:
            try:
                result = func(*command[1:])
            except TypeError as e:
                result = e
            print(result)
        elif command[0] in ['stop', 'exit', 'quit']:
            self.base.StopTaskSystem()
            print('Manager has been stopped')
            return None
        else:
            print('invalid command.')

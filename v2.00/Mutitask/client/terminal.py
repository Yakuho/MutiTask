from .functionitem import FuncItem
from threading import Thread


class Terminal:
    def __init__(self, baseConfig, funcItem):
        self.base = baseConfig
        self.FuncItem = funcItem

    def run(self):
        t1 = Thread(target=self.FuncItem.ExecuteDetect, args=())
        t2 = Thread(target=self.FuncItem.ExecuteMission, args=())
        t1.start()
        t2.start()
        t1.join()
        t2.join()

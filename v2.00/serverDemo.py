from Mutitask.server import BaseConfig
from Mutitask.server import Terminal


def task_generator(t1, t2):
    for i in range(t1, t2):
        yield f'https://kuaidaili/index{i}/'


if __name__ == '__main__':
    baseConfig = BaseConfig(deviceNumb=5)
    terminal = Terminal(baseConfig=baseConfig)
    terminal.run([task_generator(0, 10)])

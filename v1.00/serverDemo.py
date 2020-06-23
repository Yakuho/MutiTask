from Mutitask.server import Server


def task():
    for i in range(1, 100):
        yield f'https://www.kuaidaili.com/free/inha/{i}/'


# manager = Server(WorksNumb=5, TasksChannelMax=20, InstructionChannelNumb=1)
# tasks = [task()]
# manager.start(tasks)

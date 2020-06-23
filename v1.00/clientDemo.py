from Mutitask.client import Client
from requests import get


def task_function(task):
    url = task
    response = get(url)
    if response.status_code == 200:
        return response.status_code
    else:
        return None


def save_function(result):
    print(result)


a = Client(device=0)
a.initial_task_function(task_func=task_function)
a.initial_save_function(save_func=save_function)
a.start(channel=0)

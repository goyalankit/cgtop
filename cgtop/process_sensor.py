import os
import psutil
import time

from constants import RHEL6_CGROUP_PATH, RHEL7_CGROUP_PATH
from helpers import read_metric_from_file

previous_cpu_usage = 0
previous_timestamp = time.time()


class ProcessSensor:
    def get_process_data(self):
        tasks_path = os.path.join(self.task_cg_path, 'tasks')

        tasks_list = read_metric_from_file(tasks_path).split()

        process_lines = []
        for task in tasks_list:
            process = psutil.Process(int(task))

            created_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(
                    psutil.Process(process.pid).create_time
                )
            )
            process_line = "{pid} {username} {name} {created_time}".format(
                pid=process.pid, username=process.username,
                name=process.name, created_time=created_time
            )
            process_lines.append(process_line)

        return {'processes': process_lines}


class Rhel6ProcessSensor(ProcessSensor):
    def __init__(self, container):
        self.task_cg_path = os.path.join(RHEL6_CGROUP_PATH, container.name)


class Rhel7ProcessSensor(ProcessSensor):
    def __init__(self, container):
        self.task_cg_path = os.path.join(RHEL7_CGROUP_PATH, container.name)

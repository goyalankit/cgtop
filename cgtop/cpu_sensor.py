import os
import time

from constants import RHEL6_CGROUP_PATH, RHEL7_CGROUP_PATH
from decimal import Decimal
from helpers import read_metric_from_file

previous_cpu_usage = 0
previous_timestamp = time.time()


class CpuSensor:
    def get_cpu_data(self):
        cpu_usage_path = os.path.join(self.cpu_cg_path, 'cpuacct.usage')

        global previous_cpu_usage, previous_timestamp

        if previous_cpu_usage == 0:
            previous_cpu_usage = Decimal(read_metric_from_file(cpu_usage_path))
            previous_timestamp = Decimal('%.9f' % time.time()) * 10 ** 9

        current_cpu_usage = Decimal(read_metric_from_file(cpu_usage_path))
        current_timestamp = Decimal('%.9f' % time.time()) * 10 ** 9

        time_interval = current_timestamp - previous_timestamp
        cpu_usage = current_cpu_usage - previous_cpu_usage

        fraction_cpu_usage = cpu_usage / time_interval

        previous_cpu_usage = current_cpu_usage
        previous_timestamp = current_timestamp

        return {
            'fraction_cpu_usage': fraction_cpu_usage
        }


class Rhel6CpuSensor(CpuSensor):
    def __init__(self, container):
        self.cpu_cg_path = os.path.join(RHEL6_CGROUP_PATH, container.name)


class Rhel7CpuSensor(CpuSensor):
    def __init__(self, container):
        self.cpu_cg_path = os.path.join(RHEL7_CGROUP_PATH, 'cpu', container.name)

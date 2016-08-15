import os
import random

from constants import RHEL6_CGROUP_PATH, RHEL7_CGROUP_PATH
from helpers import read_metric_from_file


class MemorySensor:
    def get_memory_data(self):

        # TODO Remove Dummy data.
        if not os.path.exists(self.mem_cg_path):
            return {
                'limit_in_bytes': 100,
                'usage_in_bytes': random.randint(1, 100)
            }

        mem_limit_path = os.path.join(self.mem_cg_path, 'memory.limit_in_bytes')
        mem_usage_path = os.path.join(self.mem_cg_path, 'memory.usage_in_bytes')

        return {
            'limit_in_bytes': int(read_metric_from_file(mem_limit_path)) / 1048576,
            'usage_in_bytes': int(read_metric_from_file(mem_usage_path)) / 1048576
        }


class Rhel6MemorySensor(MemorySensor):
    def __init__(self, container):
        self.mem_cg_path = os.path.join(RHEL6_CGROUP_PATH, container.name)


class Rhel7MemorySensor(MemorySensor):
    def __init__(self, container):
        self.mem_cg_path = os.path.join(RHEL7_CGROUP_PATH, 'memory', container.name)

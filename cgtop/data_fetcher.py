import os
import random

from constants import BASE_CGROUP_PATH
from helpers import read_metric_from_file
from unicurses_helpers import show_changes


class DataFetcher:
    def __init__(self):
        self.cgroups_path = BASE_CGROUP_PATH

    def get_memory_data(self, container):
        base_memory_path = "%s/memory/%s/" % (
            self.cgroups_path, container.cgpath)
        mem_limit_path = "%s/memory.limit_in_bytes" % base_memory_path
        mem_usage_path = "%s/memory.usage_in_bytes" % base_memory_path
        if not os.path.exists(base_memory_path):
            return 100, random.randint(1, 100)

        mem_limit = int(read_metric_from_file(mem_limit_path))
        mem_usage = int(read_metric_from_file(mem_usage_path))

        return mem_limit, mem_usage

    def fetch_data(self, containers):
        #
        # TODO: fetch real data.
        #
        data = {}
        for container in containers:
            data[container] = {}
            data[container]["cpu"] = random.randint(1, 100)
            data[container]["cpu_max"] = 100

            max_mem, mem_usage = self.get_memory_data(container)
            data[container]["memory"] = mem_usage
            data[container]["memory_max"] = max_mem
        return data

    def update_my_data(self, containers):
        data_for_container = self.fetch_data(containers)
        for container in containers:
            data = data_for_container[container]
            container.update_fill_bar_data(container.cpu_fill_bar,
                                           new_data=data['cpu'],
                                           total_data=data['cpu_max'],
                                           start_text="CPU",
                                           end_text="%s/100" % data['cpu_max'])

            container.update_fill_bar_data(container.memory_fill_bar,
                                           new_data=data['memory'],
                                           total_data=data['memory_max'],
                                           start_text="Mem",
                                           end_text="%s/%s" % (
                                               data['memory'],
                                               data['memory_max']))

        show_changes()

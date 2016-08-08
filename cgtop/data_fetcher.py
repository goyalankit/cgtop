import random

from helpers import show_changes


class DataFetcher:
  def __init__(self):
    self.cgroups_path = "/sys/fs/cgroup"

  def fetch_data(self, containers):
    #
    # TODO: fetch real data.
    #
    data = {}
    for container in containers:
      data[container] = {}
      data[container]["cpu"] = random.randint(1, 100)
      data[container]["cpu_max"] = 100
      data[container]["memory"] = random.randint(1, 200)
      data[container]["memory_max"] = 200
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
                                     end_text="%s/200" % data['memory_max'])

    show_changes()

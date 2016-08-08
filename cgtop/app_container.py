from cgroup_container import CgroupContainer
from helpers import show_changes


class AppContainer(CgroupContainer):
  def __init__(self, name, path, layout, stop_event):
    CgroupContainer.__init__(self, layout, title=name)

    self.name = name
    self.path = path
    self.stop_event = stop_event

  def initialize_bars(self):
    self.title_window_on_screen()

    cpu_fill_bar = self.create_cpu_fill_bar()
    self.update_fill_bar_data(
      cpu_fill_bar,
      new_data=0, total_data=100,
      start_text="CPU", end_text="0/0"
    )

    memory_fill_bar = self.create_memory_fill_bar()
    self.update_fill_bar_data(
      memory_fill_bar,
      new_data=0, total_data=100,
      start_text="Mem", end_text="0/0"
    )

  @staticmethod
  def create_app_containers(layouts, global_stop_event):
    containers = []
    for num, layout in enumerate(layouts):
      container = AppContainer(
        "noop-app-i%s" % num,
        "/sys/fs/cgroup",
        layout, global_stop_event
      )

      container.initialize_bars()
      containers.append(container)

    show_changes()
    return containers
from cgroup_container import CgroupContainer

class AppContainer(CgroupContainer):
  def __init__(self, name, layout, stop_event):

    self.name = name
    self.layout_number = layout
    self.stop_event = stop_event
    pass






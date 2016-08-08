"""
  Class to provide the functionality of updating the stats off the main thread,
  run things as a thread job
"""

import threading


class BackgroundThread(threading.Thread):
  def __init__(self, callback, event, interval, cgroup_container):
    """runs the callback function after interval seconds

    :param callback:  callback function to invoke
    :param event: external event for controlling the update operation
    :param interval: time in seconds after which callback if fired.
    :type callback: function
    :type interval: int
    """
    self.callback = callback
    self.event = event
    self.interval = interval
    self.cgroup_container = cgroup_container
    super(BackgroundThread, self).__init__()

  def run(self):
    while not self.event.wait(self.interval):
      self.callback(self.cgroup_container)

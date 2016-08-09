"""
  Class to provide the functionality of updating the stats off the main thread,
  run things as a thread job
"""

import threading


class BackgroundThread(threading.Thread):
    def __init__(self, callback, interval, containers):
        """runs the callback function after interval seconds

        :param callback:  callback function to invoke
        :param event: external event for controlling the update operation
        :param interval: time in seconds after which callback if fired.
        :type callback: function
        :type interval: int
        """
        self.callback = callback
        self._stop = threading.Event()
        self.interval = interval
        self.containers = containers
        super(BackgroundThread, self).__init__()

    def run(self):
        while not self._stop.wait(self.interval) and not self._stop.is_set():
            self.callback(self.containers)

    def stop(self):
        self._stop.set()

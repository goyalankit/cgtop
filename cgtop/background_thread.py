import threading


class BackgroundThread(threading.Thread):
    """Provides background thread that calls callback at given interval."""
    def __init__(self, callback, interval, containers):
        """runs the callback function after interval seconds.

        :param callback: callback function to invoke on each interval
        :param interval: time in seconds after which callback if fired.
        :param containers: CgroupContainer objects to update.
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

##
## https://pythonassets.com/posts/executing-code-every-certain-time/
## some modifications were made
##

import threading
import time


class ParentTimer(threading.Thread):

    def __init__(self):
        self._timer_runs = threading.Event()
        self._timer_runs.set()
        super().__init__()

    def run(self):
        while self._timer_runs.is_set():
            self.timer()
            time.sleep(self.__class__.interval)

    def stop(self):
        self._timer_runs.clear()
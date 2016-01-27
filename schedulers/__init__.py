from time import sleep
from collections import namedtuple
from threading import Thread

class Timer(object):

    def __init__(self, interval, rid, fun):
        self.interval = interval
        self.rid = rid
        self.fun = fun

class SchedulerBase(object):

    def schedule(self, interval: int, fun):
        raise NotImplementedError

    def stop_timer(self, rid: int) -> bool:
        raise NotImplementedError

    def run(self, ticklength: int):
        while True:
            self._tick(ticklength)
            sleep(ticklength)

    def start(self, ticklength: int):
        thread = Thread(target=self.run, args=[ticklength])
        thread.start()
        return thread


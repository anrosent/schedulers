from time import sleep
from collections import namedtuple
from threading import Thread

def locked(f):
    def wr(self, *args, **kwargs):
        self.mutex.acquire()
        result = f(self, *args, **kwargs)
        self.mutex.release()
        return result
    return wr

class Timer(object):

    def __init__(self, expiry, rid, fun):
        self.expiry = expiry 
        self.rid = rid
        self.fun = fun

    def __str__(self):
        return str((self.expiry, self.rid))

    def __repr__(self):
        return str(self)

class SchedulerBase(object):

    rid_ctr = 0

    @locked
    def schedule(self, interval: int, fun) -> Timer:
        rid = self._new_rid()
        timer = self._start_timer(interval, rid, fun)
        return timer 

    @locked
    def repeat(self, interval: int, fun) -> Timer:
        rid = self._new_rid()
        def repeater():
            fun()
            self._start_timer(interval, rid, fun)

        return self._start_timer(interval, rid, repeater)
        

    def _new_rid(self):
        rid = self.rid_ctr
        self.rid_ctr += 1
        return rid

    def stop_timer(self, rid: int) -> bool:
        raise NotImplementedError

    def _tick(self, ticklength: int):
        raise NotImplementedError

    def _start_timer(self, interval: int, rid: int, fun) -> Timer:
        raise NotImplementedError

    def run(self, ticklength: int = 1):
        while True:
            self._tick(ticklength)
            sleep(ticklength)

    def start(self, ticklength: int = 1):
        thread = Thread(target=self.run, args=[ticklength])
        thread.start()
        return thread


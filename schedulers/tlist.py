from threading import Lock
from schedulers import SchedulerBase, Timer, locked

class TimerListScheduler(SchedulerBase):

    def __init__(self):
        self.mutex = Lock()
        self.timers = []
        self.rid_ctr = 0
        self.t = 0

    def _start_timer(self, interval: int, rid: int, fun) -> Timer:
        t = Timer(interval, rid, fun)
        self.timers.append(t)
        return t

    @locked
    def stop(self, rid: int) -> Timer:
        for ix, timer in enumerate(self.timers):
            if timer.rid == rid:
                break
        else:
            return None
        return self.timers.pop(ix)

    @locked
    def _tick(self, ticklength: int = 1):
        self.t += ticklength
        expired = []
        for ix, timer in enumerate(self.timers):
            if timer.interval <= self.t:
                timer.fun() 
                expired.append(ix)

        # clear timers last to first so we don't have to shift indices
        for ix in reversed(expired):
            self.timers.pop(ix)
            



from threading import Lock
from schedulers import SchedulerBase, Timer, locked

class TimerListScheduler(SchedulerBase):

    def __init__(self):
        self.mutex = Lock()
        self.rid_ctr = 0
        self.timers = []

    @locked
    def schedule(self, interval: int, fun):
        rid = self.rid_ctr
        self.timers.append(Timer(interval, rid, fun)) 
        self.rid_ctr += 1

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
        expired = []
        for ix, timer in enumerate(self.timers):
            timer.interval -= ticklength
            if timer.interval <= 0:
                timer.fun() 
                expired.append(ix)
        # clear timers last to first so we don't have to shift indices
        for ix in reversed(expired):
            self.timers.pop(ix)
            



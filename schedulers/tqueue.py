from schedulers import SchedulerBase, Timer, locked
from threading import Lock

def _insert_sorted(lst, el, cp):
    for i, e in enumerate(lst):
        if cp(el, e) <= 0:
            lst.insert(i, el)
            break
    else:
        lst.append(el)

class TimerQueueScheduler(SchedulerBase):

    def __init__(self):
        self.mutex = Lock()
        self.rid_ctr = 0
        self.timers = []

    @locked
    def schedule(self, interval: int, fun):
        rid = self.rid_ctr
        _insert_sorted(self.timers, Timer(interval, rid, fun), lambda a, b: a.interval - b.interval) 
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
            else:
                continue
        # clear timers last to first so we don't have to shift indices
        for ix in reversed(expired):
            self.timers.pop(ix)
            

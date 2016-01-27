from schedulers import SchedulerBase, Timer

class TimerListScheduler(SchedulerBase):

    def __init__(self):
        self.rid_ctr = 0
        self.timers = []

    def schedule(self, interval: int, fun):
        rid = self.rid_ctr
        self.timers.append(Timer(interval, rid, fun)) 
        self.rid_ctr += 1

    def stop(self, rid: int) -> Timer:
        for ix, timer in enumerate(self.timers):
            if timer.rid == rid:
                break
        else:
            return None
        return self.timers.pop(ix)

    def _tick(self, ticklength: int):
        expired = []
        for ix, timer in enumerate(self.timers):
            timer.interval -= ticklength
            if timer.interval <= 0:
                timer.fun() 
                expired.append(ix)
        # clear timers last to first so we don't have to shift indices
        for ix in reversed(expired):
            self.timers.pop(ix)
            



from schedulers import SchedulerBase, Timer, locked
from threading import Lock

class TimerRingScheduler(SchedulerBase):

    def __init__(self, ringsize = 64):
        self.mutex = Lock()
        self.rid_ctr = 0
        self.ring = [list() for i in range(ringsize)]
        self.t = 0

    @locked
    def stop(self, rid: int) -> Timer:
        for bucket in self.ring:
            for jx, timer in enumerate(bucket):
                if timer.rid == rid:
                    break
            else:
                continue
            return bucket.pop(jx)

    def _start_timer(self, interval: int, rid: int, fun) -> Timer:
        expiry = self.t + interval
        timer = Timer(expiry, rid, fun)
        bucket = self.ring[ (expiry) % len(self.ring) ]
        bucket.append(timer)
        return timer

    @locked
    def _tick(self, ticklength: int = 1):
        self.t += ticklength

        expired = []
        bucket = self.ring[self.t % len(self.ring)]
        for ix, timer in enumerate(bucket):
            if timer.expiry <= self.t:
                timer.fun() 
                expired.append(ix)

        # clear timers last to first so we don't have to shift indices
        for ix in reversed(expired):
            bucket.pop(ix)

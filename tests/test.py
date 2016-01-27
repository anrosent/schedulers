from schedulers.tlist import *

def tSimple(cls):
    scheduler = cls()
    sentinal = False
    def fun():
        nonlocal sentinal
        sentinal = True
    rid = scheduler.schedule(3, fun)
    for check in [False, False, True]:
        scheduler._tick(1)
        assert sentinal == check

def testTlist():
    tSimple(TimerListScheduler)

from schedulers.tlist import *
from schedulers.tqueue import *

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

#TODO: randomized, general tester
#TODO: run tester on all impls

def testTlist():
    tSimple(TimerListScheduler)

def testTQueue():
    tSimple(TimerQueueScheduler)

from random import randint

from schedulers import *
from schedulers.tlist import *
from schedulers.tqueue import *
from schedulers.tring import *

#TODO: tests for stop API
#TODO: tests in context of actual concurrency for races/deadlocks
#TODO: tests for scheduling when T != 0

N = 100

def oracle(cls, n):
    scheduler = cls()
    sentinal = []
    def check_invariant(ticks, expirys, expired):
        correct = sorted(filter(lambda i: i <= ticks, expirys))
        assert correct == expired, "%s, %s, %s" % (ticks, correct, expired)

    def funmaker(i):
        def f():
            nonlocal sentinal
            sentinal.append(i)
        return f

    expirys = [randint(1, n) for i in range(n)]
    timers = [scheduler.schedule(t, funmaker(t)) for t in expirys]

    for i in range(n):
        check_invariant(i, expirys, sentinal)
        scheduler._tick()


def testTlist():
    oracle(TimerListScheduler, N)

def testTQueue():
    oracle(TimerQueueScheduler, N)

def testTRing():
    oracle(TimerRingScheduler, N)

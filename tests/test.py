from random import randint

from schedulers import *
from schedulers.tlist import *
from schedulers.tqueue import *
from schedulers.tring import *

N = 100

def oracle(cls, n):
    scheduler = cls()
    sentinal = []
    def check_invariant(ticks, intervals, expired):
        correct = sorted(filter(lambda i: i <= ticks, intervals))
        assert correct == expired, "%s, %s, %s" % (ticks, correct, expired)

    def funmaker(i):
        def f():
            nonlocal sentinal
            sentinal.append(i)
        return f

    intervals = [randint(1, n) for i in range(n)]
    timers = [scheduler.schedule(t, funmaker(t)) for t in intervals]

    for i in range(n):
        check_invariant(i, intervals, sentinal)
        scheduler._tick()

#TODO: tests for stop API
#TODO: tests in context of actual concurrency for races/deadlocks

def testTlist():
    oracle(TimerListScheduler, N)

def testTQueue():
    oracle(TimerQueueScheduler, N)

'''
def testTRing():
    oracle(TimerRingScheduler, N)
    '''

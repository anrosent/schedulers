from random import randint

from schedulers import *
from schedulers.tlist import *
from schedulers.tqueue import *
from schedulers.tring import *

N = 100

def oracle(cls, n):
    scheduler = cls()
    sentinal = []
    def check_invariant(ticks, alltimers, expired):
        correct = filter(lambda t: t.interval <= ticks, alltimers)
        correctInts = sorted(t.interval for t in correct)
        assert correctInts == sorted(expired), "%s, %s, %s" % (ticks, correctInts, sorted(expired))

    def funmaker(i):
        def f():
            nonlocal sentinal
            sentinal.append(i)
        return f

    timers = []
    for i in range(n):
        t = randint(1, n)
        timers.append(Timer(t, i, funmaker(t)))
    for timer in timers:
        scheduler.schedule(timer.interval, timer.fun)

    for i in range(n):
        check_invariant(i, timers, sentinal)
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

from random import randint

from schedulers import *
from schedulers.tlist import *
from schedulers.tqueue import *

N = 100

def oracle(cls, n):
    scheduler = cls()
    sentinal = []
    def invariant(ticks, alltimers, expired):
        correct = filter(lambda t: t.interval <= ticks, alltimers)
        correctInts = sorted(t.interval for t in correct)
        return correctInts == sorted(expired)

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
        assert invariant(i, timers, sentinal)
        scheduler._tick()

def testTlist():
    oracle(TimerListScheduler, N)

def testTQueue():
    oracle(TimerQueueScheduler, N)

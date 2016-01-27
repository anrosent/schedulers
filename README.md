timers
===

This repo contains implementations for a couple different timer designs found [in this paper](http://www.cs.columbia.edu/~nahum/w6998/papers/sosp87-timing-wheels.pdf).

All the timers share the same API:

 - `schedule(interval: int, fun: ()=> ) -> timer_id: int`
 - `stop_timer(timer_id: int) -> found: bool`
 - `start(ticklength: int) -> threading.Thread`
    - Runs scheduler/executor loop on separate thread

#Scheduler Designs Implemented thus far
 - Timer List

#Testing

There is at least one test that passes! Run the tests like so to make sure you use the right Python version to drive `nosetests`.
```
$   python3 -m nose
```

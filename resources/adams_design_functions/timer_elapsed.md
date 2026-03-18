# TIMER_ELAPSED

Either starts or ends a timer for measuring the elapsed time in seconds.

## Format
```
TIMER_ELAPSED (endFlag) returns REAL
```

## Arguments

**endFlag**
: If the endFlag is 0, then the timer is started and the current elapsed CPU is returned. If the endFlag is 1, then the timer is stopped and the elapsed CPU time since the last timer started is returned.

# TIMER_CPU

Either starts or ends a timer for measuring the accumulated time in CPU seconds used since the beginning of the process execution.

## Format
```
TIMER_CPU(endFlag) returns REAL
```

## Arguments

**endFlag**
: If the endFlag is 0, then the timer is started and the current elapsed CPU is returned. If the endFlag is 1, then the timer is stopped and the elapsed CPU time since the last timer started is returned.

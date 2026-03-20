# TIME and PI — Built-in Constants

Adams provides two built-in constants that are always available in any `FUNCTION=` expression without arguments or object references.

## TIME

```
TIME
```

Current simulation time in the model's time unit (seconds by default). `TIME` is updated at every solver timestep.

### Common uses

```adams_fn
! Ramp force from 0 to 1000 N over the first 2 seconds
STEP(TIME, 0.0, 0.0, 2.0, 1000.0)

! Sinusoidal excitation at 10 Hz
500.0 * SIN(2.0 * PI * 10.0 * TIME)

! Apply force only after t = 0.5 s
IF(TIME - 0.5 : 0.0, 0.0, 200.0)
```

## PI

```
PI
```

The mathematical constant π ≈ 3.14159265358979. No arguments.

### Common uses

```adams_fn
! Convert 180 degrees to radians manually
PI

! Angular frequency from RPM
2.0 * PI * (1500.0 / 60.0)   ! = 157.08 rad/s

! Full-circle sweep STEP
STEP(TIME, 0.0, 0.0, 1.0, 2.0 * PI)
```

## Notes

- `TIME` and `PI` have no parentheses and no arguments — they are bare identifiers.
- The `D` suffix on angle literals (e.g., `90D`) is the preferred way to enter degree values in expressions; internally Adams converts them: `90D = PI/2`.

## See also

- [STEP](step.md) — smooth ramp using TIME
- [SHF](shf.md) — sinusoidal harmonic force
- [ABS and math functions](abs.md) — full math function reference

# TMAT3

Returns a 3x3 transformation matrix using the values in the orientation sequence you specify.

## Format
```
TMAT3 (E, OriType, OriSequence)
```

## Arguments

**E**
: 3x1 Euler orientation sequence.

**OriType**
: A single character, either "s" or "b" (character case is ignored), denoting that E contains either space- or body-based rotations.

**OriSequence**
: A three digit integer specifying the axes about which the rotations take place. 313 would indicate that E[1] rotates about Z, E[2] rotates about X and E[3] rotates about Z.

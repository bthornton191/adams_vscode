# LOC_SPHERICAL

Returns Cartesian coordinates (x, y, z) that are equivalent to spherical coordinates (,  ,  ). In this case:

## Format
```
LOC_SPHERICAL (Rho, Theta, Phi)
```

## Arguments

**Rho**
: The radius of the sphere.

**Theta**
: Counterclockwise rotation about y

**Phi**
: Counterclockwise rotation about z

## Example

The following example illustrates the use of the LOC_SPHERICAL function:

### Function
```
LOC_SPHERICAL(10, 8D, 90D)
```

### Result
```
9.9, 1.39, 0
```

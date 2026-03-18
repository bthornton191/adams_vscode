# HOT_SPOTS

Returns all spots on the body that exceed the specified threshold value.

## Format
```
HOT_SPOTS(Body_or_{Body [, Analysis]}, Value_or_{Value [, Type]}, {Threshold, Radius [, Start, End]})
```

When an array argument contains only one element, it can be passed as a scalar without braces.

## Arguments

**Name array**: `Body` or `{Body, Analysis}`

**Body**
: Name of flexible body or part with a rigid stress object.

**Analysis**
: Name of analysis (optional).

---

**Integer array**: `Value` or `{Value, Type}`

**Value**
: Flag for the value of stress or strain to use.

**Type**
: Flag for stress (1) or strain (2) (optional). Default is stress (1).

---

**Real array**: `{Threshold, Radius [, Start, End]}`

**Threshold**
: Return all hot spots that exceed this value.

**Radius**
: Minimum distance between hot spots (unit of length).

**Start**
: Time to start checking for hot spots (optional). Default is the beginning of the analysis.

**End**
: Time to stop checking for hot spots (optional). Default is the end of the analysis.

## Returns

Real 6xN array — N rows of hot-spot data:

* **[1-3]** X, Y, Z: Location of hot spot on body (with respect to LPRF).
* **[4]** Time: Time when the maximum value occurred.
* **[5]** Value: Maximum value at the hot spot.
* **[6]** Node: Node ID of the hot spot.

## Example

Locate hot spots in a part called `shaft` where the maximum von Mises stress exceeds 700 MPa, for the analysis `engine_stall`, with points at least 25 mm apart:

```
VAR SET VAR=hotspots REAL=(EVAL(HOT_SPOTS({shaft,engine_stall}, {0,1}, {700.0,25.0})))
```

Because `engine_stall` was the default analysis and the default stress flag is 1, this can be simplified to:

```
VAR SET VAR=hotspots REAL=(EVAL(HOT_SPOTS(shaft, 0, {700,25})));
```



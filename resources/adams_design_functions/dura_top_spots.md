# TOP_SPOTS

Returns a fixed number of the hottest spots in the body.

## Format
```
TOP_SPOTS(Body_or_{Body [, Analysis]}, Value_or_{Value [, Type]}, {Percent, Radius [, Start, End]}, Count)
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

**Real array**: `{Percent, Radius [, Start, End]}`

**Percent**
: Number of hot spots to return, expressed as a percentage (%). If set to zero (0.0), the Count argument is used.

**Radius**
: Minimum distance between hot spots (unit of length).

**Start**
: Time in the analysis to start checking for hot spots (optional). Default is the beginning of the analysis.

**End**
: Time in the analysis to end checking for hot spots (optional). Default is the end of the analysis.

---

**Count**
: Number of hot spots to return (used when Percent is 0).

## Returns

Real 6xN array — N rows of hot-spot data:

* **[1-3]** X, Y, Z: Location of hot spot on body (with respect to LPRF).
* **[4]** Time: Time when the maximum value occurred.
* **[5]** Value: Maximum value at the hot spot.
* **[6]** Node: Node ID of the hot spot.

## Example

Return the maximum principal stress in the `link` part, along with the node and time of peak stress:

```
VAR SET VAR=topspot REAL=(EVAL(TOP_SPOTS(link,{7,1},{0,0.0},1)));
VAR SET VAR=maxstress REAL=(topspot.real_value[5]) UNITS=PRESSURE;
VAR SET VAR=maxnode INT=(topspot.real_value[6]);
VAR SET VAR=maxtime REAL=(topspot.real_value[4]) UNITS=TIME;
```

The location of maximum stress can also be extracted as real values 1, 2, and 3.



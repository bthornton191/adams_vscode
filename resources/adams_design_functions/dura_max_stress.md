# MAX_STRESS

Returns the maximum value of stress for the body for the default analysis.

## Format
```
MAX_STRESS(Body_or_{Body [, Analysis]}, Criterion_or_{Criterion [, Type]})
```

When an array argument contains only one element, it can be passed as a scalar without braces.

## Arguments

**Name array**: `Body` or `{Body, Analysis}`

**Body**
: Name of the flexible body or part with a rigid stress object.

**Analysis**
: Name of the analysis (optional). Defaults to the current analysis.

---

**Integer array**: `Criterion` or `{Criterion, Type}`

**Criterion**
: Stress criterion to evaluate (e.g. von Mises, maximum principal).

**Type**
: Flag for stress (1) or strain (2) (optional). Default is stress (1).

## Returns

Real — the maximum stress value across all nodes of the body.



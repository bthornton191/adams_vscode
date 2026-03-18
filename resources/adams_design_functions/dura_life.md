# LIFE

Returns the minimum fatigue life of a flexible body for the specified analysis.

## Format
```
LIFE(FlexBody_or_{FlexBody [, Analysis]})
```

When the array contains only one element, it can be passed as a scalar without braces.

## Arguments

**Name array**: `FlexBody` or `{FlexBody, Analysis}`

**FlexBody**
: Name of the flexible body.

**Analysis**
: Name of the analysis (optional). Defaults to the current analysis.

## Returns

Real — the minimum fatigue life value across all nodes of the flexible body.



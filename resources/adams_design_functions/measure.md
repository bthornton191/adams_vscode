# MEASURE

The MEASURE performs calculations using simulation results. The calculations that can be specified are equivalent to the characteristics that can be measured using Object Measures.

## Format
```
MEASURE (object, CoordSystem, RefFrame, characteristic, component)
```

## Arguments

**object**
: The object that the user is measuring

**CoordSystem**
: Enter the marker on which the vector quantity is projected. The default is the global coordinate system.

**RefFrame**
: The reference frame in which any time derivatives needed to compute the measure quantity will be computed. The RefFrame can be thought of the reference frame which the 'observer' is fixed in.

**characteristic**
: The characteristic to be measured. Available characteristics for an object are displayed in the characteristic list of the plot builder when the object is selected in the object list.

**component**
: The component of characteristic to be measured. Available components for an object/characteristic combination can be viewed in the component list of the plot builder when the object and characteristic are picked in their respective lists.

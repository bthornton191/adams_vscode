# Array HOT_SPOTS (Name array, Integer array, Real array)

Returns all of the spots on the Body that exceed the specified Threshold. 

## Arguments

**Name**
: array 

**Body**
: Name of flexible body or part with a rigid stress object.

**Analysis**
: Name of analysis (optional)

**Integer**
 array 

**Value**
: Flag for value of stress or strain to use.

**Type**
: Flag for stress (1) or strain (2) (optional). Default is stress (1).

**Real**
 array 

**Threshold**
: Return all hot spots that exceed this value.

**Radius**
: Distance between hot spots (unit of length).

**Start**
: Time to start checking for hot spots (optional). Default is the beginning of the analysis.

**End**
: Time to stop checking for hot spots (optional). Default is the end of the analysis.

## Returns

Real 6 x N array - N rows of hot-spot data with the following information: 

* X, Y, Z: Location of hot spot on body, with respect to local part reference frame (LPRF).

* Time: Time when the maximum value occurred.

* Value: Maximum value of hot spot.

* Node: Node ID of hot spot.
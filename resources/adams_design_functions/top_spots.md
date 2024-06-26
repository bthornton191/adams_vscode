# Array TOP_SPOTS (Name array, Integer array, Real array)

Returns a fixed number of the hottest spots in the Body. 

## Arguments

**Name**
: array 

**Body**
: Name of flexible body or part with a rigid stress object.

**Analysis**
: Name of analysis (optional)

**Integer**
: array 

**Value**
: Flag for value of stress or strain to use.

**Type**
: Flag for stress (1) or strain (2) (optional). Default is stress (1).

**Real**
 array

**Percent**
: Number of hot spots to return, expressed as a percentage (%). If set to zero (0.0), the count argument is used to determine how many to return.

**Radius**
: Distance between hot spots (unit of length).

**Start**
: Time in the analysis to start checking for hot spots (optional). Default is the beginning of the analysis (unit of time).

**End**
: Time in the analysis to end check for hot spots (optional). Default is the end of the analysis (unit of time).

**Count**
: Number of hot spots to return.

## Returns

Real 6xN array - N rows of hot-spot data with the following information: 

* X, Y, Z: Location of hot spot on body (with respect to LPRF).
* Time: Time when the maximum value occurred.
* Value: Maximum value of hot spot.
* Node: Node ID of hot spot.

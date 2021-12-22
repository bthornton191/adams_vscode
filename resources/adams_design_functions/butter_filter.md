# BUTTER_FILTER

Filter a curve with the Butterworth filter specified by the order and cutoff frequency. 

## Format 
```java
BUTTER_FILTER (x, y, fType, order, cutoff, isAnalog, isTwoPass) returns ARRAY 
```
## Argument 

 



**x**
: An array of the x-axis of the curve, usually time.  


**y**
: An array of the y-axis of the curve. 


**fType**
: A text string. The filter type, can be one of 
* low
* high
* pass
* stop 


**order**
: An integer indicating the order of the Butterworth filter.  


**cutoff**
: An array. The cutoff frequency can have one or two elements. Here the cutoff frequency does not normalize.  


**isAnalog**
: A Boolean value indicating whether it uses analog filtering. 


**isTwoPass**
: A Boolean value indicating whether it uses zero-phase filtering. 

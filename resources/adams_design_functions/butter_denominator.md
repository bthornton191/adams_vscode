# BUTTER_DENOMINATOR 

Calculates the denominator coefficients for the Butterworth filter. 

## Format 
```java
BUTTER_DENOMINATOR (n, wn, fType, isDigital) returns ARRAY 
```
## Argument 

 



**n**
: An integer value indicating the order of the Butterworth filter.  


**wn**
: Array of values indicating the cutoff frequency that can have one or two elements. 


**fType**
: A text string. The filter type, can be one of :
* low
* high
* pass
* stop


**isDigital**
: A Boolean value.  


## Example 

The following example illustrates the **BUTTER_DENOMINATOR** function:

 



## Function  
```java
butter_denominator(6, {0.1951, 0.4081}, "pass", 1)  
```

## Result  
```java
{1.0000, -5.8240, 17.6909, -35.8509, 53.4731, -61.3642, 55.3780, -39.5185, 22.1585, -9.5439, 3.0209, -0.6376, 0.0708}  
```
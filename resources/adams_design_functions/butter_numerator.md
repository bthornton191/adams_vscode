# BUTTER_NUMERATOR

Returns an array of the numerator coefficients for the Butterworth filter. 

## Format 
```java
BUTTER_NUMERATOR (n, wn, fType, isDigital) 
```
## Arguments 

 



**n**
: An integer value indicating the order of the Butterworth filter. 


**wn**
: An array of values indicating that the cutoff frequency can have one or two elements. 


**fType**
: A text string. The filter type, can be one of 
* low
* high
* pass
* stop  


**isDigital**
: A Boolean value. 


## Example 

The following example illustrates the **BUTTER_NUMERATOR** function:

 



### Function  
```java
butter_numerator (6, {0.1951, 0.4081}, "pass", 1)  
```

### Result  
```java
{0.0005, 0, 0.0070, 0, -0.0094, 0, 0.0070, 0, -0.002, 8, 0,0.005}  
```
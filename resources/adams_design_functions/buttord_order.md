# BUTTORD_ORDER

Returns the order for the Butterworth filter. 

## Format 
```java
BUTTORD_ORDER (wp, ws, rp, rs, isDigital)
```
## Arguments 

 



**wp**
: ARRAY: Passband corner frequency. wp, the cutoff frequency, has a value between 0 and 1, where 1 corresponds to half the sampling frequency (the Nyquist frequency).  


**ws**
: ARRAY: Stopband corner frequency. ws is in the same units as wp; it has a value between 0 and 1, where 1 corresponds to half the sampling frequency (the Nyquist frequency).  


**rp**
: REAL: Passband ripple, in decibels. This value is the maximum permissible passband loss in decibels. The passband is 0<w<1p.  


**rs**
: REAL: Stopband attenuation, in decibels. This value is the number of decibels the stopband is down from the passband. The stopband is Ws<w<1.  


**isDigital**
: A Boolean value. 


## Example 

The following is an illustration of the **BUTTORD_ORDER** function:

 



### Function  
```java
buttord_order ({0.2, 0.4}, {0.1, 0.5}, 3.0, 30.0, 1)  
```

### Result  
```java
6 
```

 



>Note:   
>wp and ws must have the same array size, either one or two.

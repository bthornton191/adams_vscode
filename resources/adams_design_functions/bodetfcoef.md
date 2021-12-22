# BODETFCOEF

Returns the gain and/or phase values for the frequency response function of a transfer function specified by its numerators and denominators. 

## Format 
```java
BODETFCOEF (OUTTYPE, NUMER, DENOM, FREQSTART, FREQEND, FREQARG) 
```
## Arguments 

 



**OUTTYPE**
: Flag used to determine whether to return gain data, phase data, or both. For additional information, see **OUTTYPE** Values.  


**NUMER**
: A 1xN array of transfer function numerators.  


**DENOM**
: A 1xN array of transfer function denominators. 


**FREQSTART**
: First frequency of requested range. 


**FREQEND**
: Last frequency of requested range.  


**FREQARG**
: Frequency count that depends on the **OUTTYPE**. When **OUTYPE** is 0,1 or 2, **FREQARG** is the step size. When **OUTTYPE** is a number between 4 and 8, **FREQARG** is the number of samples.  


## Examples 

You can create Bode data with 100 logarithmically-spaced samples between .01 and 10, by writing the following command: 
```java
var set var=bode_log_mag &
    real=(BODETFCOEF(7, {[0.01]}, {[1. , 0.4 , 1.14 , 0.22]}, 0.01, 10, 100)) 
```
Using the **OUTTYPE** Key 

The **OUTTYPE** key controls the frequencies at which Adams View computes the Bode data. In the example above, we used **OUTTYPE**=7 for logarithmically-spaced gain values. 

If you want to generate an array of the corresponding frequencies, write the following command: 
```java
var set var=log_freq &
    real=(10**series(-2., 0.030303, 100))
```
To sample on a linear scale, write the following command: 
```java
var set var=bode_log_mag &
    real=(BODETFCOEF(4, {[0.01]}, {[1. , 0.4 , 1.14 , 0.22]}, 0.01, 10, 100))
```
To generate the corresponding frequencies, write the following command: 
```java
var set var=lin_freq &
    real=(series(0.01, 0.100909, 100))
```
# BODESEQ

Returns the gain and/or phase values calculated from two sequences of time-based values describing the input and output of a linear system. The sequences are 1xN arrays of time data or measure entities. 

## Format 
```java
BODESEQ (OUTTYPE, SEQ1, SEQ2, NUMOUT) 
```
## Arguments

 



**OUTTYPE** 
: Flag used to determine whether to return gain data, phase data, or both. For additional information, please see **OUTTYPE** Values. 


**SEQ1**
: A 1xN array of time-dependent values. A measure element may be used in place of an array.  


**SEQ2**
: A 1xN array of time-dependent values. A measure element may be used in place of an array.  


**NUMOUT**
: Integer number of requested output values. 


## Extended Definition 

When a Bode plot is generated for two sequences of values, the sequences are assumed to be the input to a linear system and the output that corresponds to that input. The sequences are the excitation of the linear system and the response due to that excitation. 

Adams View computes a Fast Fourier Transform (FFT) of the two sequences and the Bode plot is simply the magnitude and the phase of the complex ratio of the output FFT to the input FFT. 
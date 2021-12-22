# BODEABCD

Returns gain and/or phase values for the frequency response function for a linear system specified by ABCD linear state matrices. 

## Format
```java
BODEABCD (OUTTYPE, OUTINDEX, A, B, C, D, FREQSTART, FREQEND, FREQARG)
```
## Arguments

 



**OUTTYPE** 
: Flag used to determine whether to return gain data, phase data, or both. 
> **OUTTYPE Values**
> 
>The value of OUTTYPE serves as a key to control the type of sampling that Adams View has to do (linear step size, linear sample count or logarithmic sample count) and whether the gain, the phase, or both are computed. When both the gain and the phase are computed, all the gains are followed by all the phases, which is rarely convenient. We recommend that you compute gain and phase separately, unless CPU time dictates taking advantage of the efficiencies of computing both at once. The following table explains the values of OUTTYPE:  
>|                | Fixed linear spacing per FREQARG    | FREQARG linearly-spaced samples     | FREQARG logarithmically-spaced samples|
>|----------------|-------------------------------------|-------------------------------------|---------------------------------------|
>| Gain and Phase | 0                                   | 3                                   |     6                                 |
>| Gain           | 1                                   | 4                                   |     7                                 |
>| Phase          | 2                                   | 5                                   |     8                                 |



**OUTINDEX**
: Index used to determine whether to return all outputs or a particular one. Index values are as follows:
* OUTINDEX = 0 (all outputs are returned) 
* OUTINDEX > 0 (nth output is returned)  


**A, B, C, D** 
: Adams View matrices containing linear state matrices.  


**FREQSTART** 
: First frequency of requested range. 


**FREQEND** 
: Last frequency of requested range. 


**FREQARG** 
: Frequency count that depends on **OUTTYPE**. When **OUTYPE** is 0,1 or 2, **FREQARG** is the step size. When **OUTTYPE** is a number between 4 and 8, **FREQARG** is the number of samples.  


## Examples

The following example assumes that you have four Adams View matrices, ABCD, as follows: 
```java
data_element create matrix full &
   matrix_name = .model_1.A &
   input_order = by_row &
   row_count = 3 &
   column_count = 3 &
   values = 0.0,  1.0, 0.0, 0.0,  0.0, 1.0, -0.22,-1.14,-0.4

data_element create matrix full &
   matrix_name = .model_1.B &
   input_order = by_column &
   row_count = 3 &
   column_count = 1 &
   values = 0.0, 0.0, 1.0

data_element create matrix full &
    matrix_name = .model_1.C &
    input_order = by_row &
    row_count = 1 &
    column_count = 3 &
    values = 0.01, 0.0, 0.0

data_element create matrix full &
    matrix_name = .model_1.D  &
    input_order = by_column &
    row_count = 1 &
    column_count = 1 &
    values = 0.0
```
Because the four matrices are equivalent to the transfer function used in the **BODETFCOEF** and **BODETFS** examples, you will get identical results when you write the following command (see Using the **OUTTYPE** Key): 
```java
var set var=bode_mag_log real=(BODEABCD(7, 1, .model_1.A, &    .model_1.B, .model_1.C, .model_1.D, 0.01, 10, 100))
```
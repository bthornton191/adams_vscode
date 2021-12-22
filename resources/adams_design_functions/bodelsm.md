# BODELSM

Computes the Bode response for a given set of A, B, C, and D matrices. These matrices are usually produced as the result of a linear system analysis. 

## Format 
```java
BODELSM (resultType, outIndex, LSM, freqStart, freqEnd, freqStep) 
```
## Arguments 

 



**resultType** 
: Specifies the components for BODELSM to return, and how the freqStep argument is used. Below are the values and their meaning: 

| Value | Returned values | Step computation           |
|-------|-----------------|----------------------------| 
|0      | mag and phase   | Fixed frequency step       |
|1      | mag only        | Fixed frequency step       |
|2      | phase only      | Fixed frequency step       |
|3      | mag and phase   | Linear sample count        |
|4      | mag only        | Linear sample count        |
|5      | phase only      | Linear sample count        |
|6      | mag and phase   | Logarithmic sample count   |
|7      | mag only        | Logarithmic sample count   |
|8      | phase only      | Logarithmic sample count   |



**outIndex** 
: Specifies the row of the two-dimensional output matrix that is to be returned. 

* **OUTINDEX** = 0 (all outputs are returned) 

* **OUTINDEX** > 0 (nth output is returned) 

If both phases and magnitudes are to be returned, then there are two rows for each input/output combination and the magnitudes are stored first.  


**LSM**
: The Adams View linear state matrix object containing the matrices computed by the system linearization.  


**freqStart** 
: Low frequency in the omega vector. 


**freqEnd**
: High frequency in omega.  


**freqStep**
: Depending on the value of resultType, this can denote either the number of samples, the linear step size, or a logarithmic step size. 

* For a fixed frequency step, this value is the actual step size of the omega vector. For example, if freqStart is given as 10 and freqEnd is 20, a value of 2 for freqStep produces sample frequencies of 10, 12, 14, 16, 18, and 20.

* For linear sample count, this value denotes the number of intervals in the omega vector, and is used to compute a linear step size. Using the same example from above, but with freqStep =5, we get 10, 12.5, 15, 17.5, and 20.

* For logarithmic sample count, the behavior is similar to the linear sample count, but the increments are used for the exponent resulting in a logarithmic progression. Using the same values supplied in the previous example, the sample becomes 10.0, 11.9, 14,1, 16.8, and 20.0. 


## Examples 
```java
simulation single statematrix & 
    state_matrices_name=.model_1.Analysis.Stmat_1 &
    plant_input_name = .model_1.pinput & 
    plant_output_name =.model_1.poutput
```
If the system has a pair of inputs and a pair of outputs, there will be four response curves, corresponding to the row indices as follows: 

* row 1 = input 1/output 1
* row 2 = input 1/output 2
* row 3 = input 2/output 1
* row 4 = input 2/output 2
```java
var create var=mags  rea=(BodeLSM (4, 3, Stmat_1, 1, 100, 50))
```
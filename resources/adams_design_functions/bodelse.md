# BODELSE

Returns output gain and/or phase values for the frequency response function for an Adams View linear state equation element. 

## Format
```java
BODELSE (OUTTYPE, OUTINDEX, O_LSE, FREQSTART, FREQEND, FREQARG) 
```
## Arguments

 



**OUTTYPE**
: Flag used to determine whether to return gain data, phase data, or both. For additional information, see **OUTTYPE** Values.  


**OUTINDEX** 
: Index used to determine whether to return all outputs or a particular one. Index values are as follows:
* **OUTINDEX** = 0 (all outputs are returned) 
* **OUTINDEX** > 0 (nth output is returned)  


**O_LSE** 
: Adams linear state equation entity.  


**FREQSTART** 
: First frequency of requested range.  


**FREQEND** 
: Last frequency of requested range. 


**FREQARG** 
: Frequency count that depends on the **OUTTYPE**. When OUTYPE is 0,1 or 2, FREQARG is the step size. When **OUTTYPE** is a number between 4 and 8, **FREQARG** is the number of samples. 


## Examples

In the following example, the ABCD matrices from `BODEABCD` are encapsulated in an Adams linear state equation element, as follows: 
```java
model create model=model_1

measure create function  &
   measure_name = .model_1.MEASURE_1  &
   function = ""  &
   units = no_units &
   create = no 

data_element create array x_state_array  &
   array_name = .model_1.x  &
   size = 3

data_element create array y_output_array  &
   array_name = .model_1.y  &
   size = 1

data_element create array u_input_array  &
   array_name = .model_1.u  &
   size = 1  &
   variable_name = .model_1.MEASURE_1 

part create equation linear_state_equation  &
   linear_state_equation_name = .model_1.LSE  &
   x_state_array_name = .model_1.x  &
   u_input_array_name = .model_1.u  &
   y_output_array_name = .model_1.y  &
   a_state_matrix_name = .model_1.A  &
   b_input_matrix_name = .model_1.B  &
   c_output_matrix_name = .model_1.C  &
   static_hold = on 
```
Because the four matrices are equivalent to the transfer function used in the **BODETFCOEF** and **BODETFS** examples, you will get identical results when you write the following command (see Using the **OUTTYPE** Key): 
```java
variable set variable=bode_mag_log real=(BODELSE(7, 1, .model_1.lse, 0.01, 10, 100))
```
# BODETFS

Returns the gain and/or phase values for the frequency response function of an Adams transfer function element. 

## Format 
```java
BODETFS (OUTTYPE, TFSISO, FREQSTART, FREQEND, FREQSTEP) 
```
## Arguments 

 



**OUTTYPE**
: Flag used to determine whether to return gain data, phase data, or both. For additional information, see **OUTTYPE** Values.  


**TFSISO**
: An Adams transfer function entity.  


**FREQSTART**
: First frequency of requested range. 


**FREQEND**
: Last frequency of requested range. 


**FREQSTEP**
:  Frequency count that depends on the **OUTTYPE**. When **OUTTYPE** is 0,1 or 2, FREQARG is the step size. When **OUTTYPE** is a number between 4 and 8, FREQARG is the number of samples.  


## Examples 

The following function assumes that you created an Adams transfer function element, as follows: 
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

part create equation transfer_function  & 
    transfer_function_name = .model_1.TRANSFER_FUNCTION_1 &
    x_state_array_name = .model_1.x  &
    u_input_array_name = .model_1.u  &
    y_output_array_name = .model_1.y  &
    static_hold = on  &
    numerator_coefficients = 0.01  &
    denominator_coefficients = 1.0, 0.4, 1.14, 0.22
```
Because the transfer function is equivalent to the four matrices used in the **BODEABCD** and **BODELSE** examples, you will get identical results when you write the following command (see Using the **OUTTYPE** Key): 
```java
variable set variable=bode_mag_log &
    real=(BODETFS(7, .model_1.TRANSFER_FUNCTION_1, 0.01, 10.0, 100))
```
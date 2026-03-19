# executive_control set easy_dynamics

The EXECUTIVE_CONTROL SET EASY_DYNAMICS command provides an automatic way to select integration attributes with a single command. In addition, this command provides an easy-to-understand method for controlling the error.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `model_name` | An existing model | Specifies the model to be modified. You use this parameter to identify the existing model to be affected with this command. |
| `significant_digits` | real | Defines the tolerance of the integration error in decimal digits of accuracy. The relative, local truncation errors for the integrator will be bounded by 5 * (0.1 ** r), where r is the specified value for the SIGNIFICANT_DIGITS argument. |
| `dynamic_attribute` | STIFF/HIGH_FREQUENCIES/ SMOOTH | Indicates the characteristics of the mechanism to be simulated. |

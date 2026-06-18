# EVAL

Evaluates a character string expression and returns the result. Commonly used in macros to dynamically evaluate expressions stored in string variables.

## Format
```adams_cmd
eval(expr_string)
```

## Arguments

**expr_string**
: A character string or string variable containing a valid Adams View expression.

## Examples

### Evaluating a literal string expression
```adams_cmd
eval("2 + 2")
```
Result: `4`

### Evaluating a string variable
```adams_cmd
variable set variable_name=my_string string_value="1.0 + 2.0"
variable set variable_name=result real_value=(eval(my_string))
```
`eval(my_string)` reads the string stored in `my_string` and evaluates it as an expression, returning `3.0`.

### Evaluating a local macro variable (avoiding parametric links)
```adams_cmd
variable set variable_name=$_self.stiffness real_value=1.0e5

force create element_like translational_spring_damper &
    spring_damper_name=.model.my_spring &
    stiffness=(eval($_self.stiffness))
```
Wrapping the local variable in `eval()` passes its numeric value to the command rather than a reference. Adams does not create a parametric link, so the local variable can be safely discarded when the macro completes.

### Evaluating a model design variable
```adams_cmd
variable set variable_name=.model.my_var real_value=500.0

force create element_like translational_spring_damper &
    spring_damper_name=.model.my_spring &
    stiffness=(eval(.model.my_var))
```
Same pattern with a model-level variable. The spring receives the current numeric value of `.model.my_var` at the time the command runs, with no ongoing parametric link to it.

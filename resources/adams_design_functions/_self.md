# $_self

Special macro variable that resolves to the full path of the macro currently being executed. It is most commonly used to create design variables scoped to the macro itself, so they act as local variables that do not exist under the model and do not interfere with model objects or existing variables.

## Usage
```adams_cmd
$_self
```

## Example

```adams_cmd
variable set variable_name=$_self.stiffness real_value=1.0e5
variable set variable_name=$_self.damping real_value=100.0
```

When referencing local variables in a modeling command, always wrap them in `eval()` so Adams receives the numeric value rather than a reference to the variable:

```adams_cmd
! CORRECT — eval() resolves the value at call time; no parametric link is created
force create element_like translational_spring_damper &
    spring_damper_name=.model.my_spring &
    i_marker_name=.model.ground.mrkr_i &
    j_marker_name=.model.body.mrkr_j &
    stiffness=(eval($_self.stiffness)) &
    damping=(eval($_self.damping))
```

```adams_cmd
! WRONG — Adams parameterizes the spring against the local variables.
! Adams will refuse to delete the variables while the spring references them,
! and the spring will update if the variables ever change.
force create element_like translational_spring_damper &
    spring_damper_name=.model.my_spring &
    i_marker_name=.model.ground.mrkr_i &
    j_marker_name=.model.body.mrkr_j &
    stiffness=$_self.stiffness &
    damping=$_self.damping
```

## Notes

- `$_self` is only meaningful inside a macro definition. Using it outside a macro context has no effect.
- The Adams VS Code extension's **Run Selection** feature automatically substitutes `$_self` with the appropriate value before sending the selected code to Adams View.

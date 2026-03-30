# Scripting — CMD Reference (Macros, Variables, Loops, Conditionals)

Adams CMD scripting lets you build **parameterized, reusable model-building procedures** using variables, loops, conditionals, and macros.

---

## Variables

### Real (numeric) variable

```cmd
variable set variable_name = .model.par_len  real_value = 250.0
variable set variable_name = .model.n_links  real_value = 6
```

- Variables persist for the duration of the Adams View session or model.
- Reference in expressions: `eval(.model.par_len)` inside a command string.

### String variable

```cmd
variable set variable_name = my_part_name  string_value = "LINK_A"
```

- Reference by full path: `(eval(.model.my_part_name))`.

### Integer variable

```cmd
variable set variable_name = .model.num_links  integer_value = 5
```

### Object variable

```cmd
variable set variable_name = .model.active_part  object_value = .model.link_1
```

- Stores a reference to an Adams object. Useful for passing parts or markers as parameters in macros.

---

## String Concatenation and Conversion

| Operator / Function | Purpose | Example |
|---------------------|---------|---------|
| `//` | Concatenate strings | `".model.link_" // RTOI(i)` |
| `RTOI(x)` | Real-to-integer string conversion | `RTOI(3)` → `"3"` |
| `EVAL(expr)` | Evaluate an expression inside a command | `EVAL(.model.n_links)` |

```cmd
! Build part name dynamically inside a loop
part create rigid_body name_and_position &
    part_name = (eval(".model.link_" // RTOI(i))) &
    ...
```

---

## Conditional: IF / END

```cmd
if condition = (DB_EXISTS(".model.link_a"))
    ! Runs only if .model.link_a already exists
    part modify rigid_body name_and_position &
        part_name = .model.link_a &
        location  = 0, 0, 100
end
```

- `DB_EXISTS("name")` returns 1 if the named object exists, 0 otherwise.
- Condition is any Adams expression enclosed in parentheses; non-zero = true.
- Multi-branch: use nested `if / end` blocks (no `else` keyword in CMD).

---

## Loop: FOR / END

```cmd
for variable_name = i  start_value = 1  end_value = (eval(.model.n_links))
    variable set variable_name = .model.cur_z  real_value = (i * 100.0)

    part create rigid_body name_and_position &
        part_name = (eval(".model.link_" // RTOI(i))) &
        location  = 0.0, 0.0, (eval(.model.cur_z))

    marker create &
        marker_name = (eval(".model.link_" // RTOI(i) // ".pin_mkr")) &
        location    = 0.0, 0.0, 0.0
end
```

- `variable_name` — the loop variable name (used with bare name inside the loop).
- `start_value` / `end_value` — numeric expressions (use `eval()` for variable references).
- Step defaults to 1; add `increment_val = 2` for step size 2.

---

## Checking if Objects Exist

```cmd
! DB_EXISTS returns 1/0
if condition = (DB_EXISTS(".model.my_spring"))
    force delete force_name = .model.my_spring
end
```


---

## Printing Debug Output

```cmd
! Print a message to the Message Window
interface statusbar status = "Building link 3 of 6..."
```

---

## See also

- [Model, Parts, and Markers](model-parts-markers.md)
- [Macros — create, parameters, file-based](macros.md)
- [Parametric chain example](../../assets/cmd_scripts/parametric_chain.cmd)

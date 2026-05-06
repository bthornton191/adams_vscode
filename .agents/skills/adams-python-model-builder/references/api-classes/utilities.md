# Session Utilities — Python API Reference

> **Authoritative stubs**: `references/adamspy-stubs/Adams.pyi`, `Expression.pyi`, `Defaults.pyi`

---

## Top-level Module Attributes

```python
import Adams

Adams.Models          # ModelManager — create/access models
Adams.defaults        # AdamsDefaults — units, coordinate system, active model
Adams.preferences     # SessionPreferences
Adams.Groups          # GroupManager
Adams.Libraries       # Library manager
Adams.Materials       # Global materials
Adams.Colors          # Color definitions
Adams.DBRoot          # Root database object
```

---

## Model Access

```python
# Get the currently active model
m = Adams.defaults.model
m = Adams.getCurrentModel()

# Create a new model
m = Adams.Models.create(name='MODEL_1')

# Load from .adm file
m = Adams.Models.newFromAdm(model_name='imported', file_name='path/to/model.adm')
```

---

## Expression Handling

```python
from Adams import expression, eval as adams_eval

# Parametric — stores the expression string; re-evaluates when referenced values change
marker.location = expression('{0, 0, .MODEL.DV_HEIGHT}')

# Evaluate once — computes value immediately, stores result
marker.location = adams_eval('.MODEL.DV_X')

# Evaluate and return value to Python
val = Adams.evaluate_exp('.MODEL.DV_K')        # returns Any
val = Adams.evaluate_real_exp('.MODEL.DV_K')   # returns float or list of float
```

**`Adams.expression()` vs `Adams.eval()`**:
- `expression(str)` → `AdamsExpr` — deferred, stays parametric; use for design variable linkage.
- `eval(str)` → computed value — evaluated once at time of assignment; not parametric after assignment.
- Direct Python value → constant stored directly.

---

## String-to-Object Lookup

```python
# Get any Adams object by its full dot-path name
obj = Adams.stoo('.MODEL_1.PART_1.MARKER_1')
mkr = Adams.stoo('.MY_MODEL.ground.ref_mkr')
```

Returns an `Object.Object` instance; cast or assign to the expected type.

---

## CMD Language Bridge

Execute Adams View CMD language commands from Python:

```python
Adams.execute_cmd('model create model_name=MODEL_1')
Adams.execute_cmd('simulation single_run transient type=auto_select '
                  'end_time=5.0 number_of_steps=500 model_name=.MY_MODEL '
                  'initial_static=no')
```

Use this as a fallback for features not yet exposed in the Python API.

---

## Switching Between Python and CMD

From Python, switch to CMD language (for the remainder of the script or until switched back):
```python
Adams.switchToCmd()
```

From CMD, switch back to Python:
```cmd
language switch_to python
```

---

## File I/O

### Binary Database (`.bin`)
```python
Adams.write_binary_file('model_snapshot.bin')
Adams.read_binary_file('model_snapshot.bin')
```

### Command File (`.cmd`)
```python
Adams.write_command_file(file_name='export.cmd', model=m)
Adams.read_command_file('existing_model.cmd')
```

### Dataset File (`.adm`)
```python
m.exportAdmFile(file_name='output.adm')
```

### Geometry Files (CAD import/export)
```python
# Import
Adams.read_geometry_file(type_of_geometry='stp', file_name='body.step',
                         part_name='.MODEL.PART_1')

# Export
Adams.write_geometry_file(type_of_geometry='stp', file_name='output.step',
                          model_name='MODEL_1')

# Allowed types: 'catiav4', 'catiav5', 'catiav6', 'igs', 'inventor', 'acis',
#                'proe', 'solidworks', 'stp', 'unigraphics', 'jt', 'dxf', 'dwg'
```

### Parasolid Files
```python
Adams.read_parasolid_file(file_name='body.xmt_txt', part_name='.MODEL.PART_1')
Adams.write_parasolid_file(file_name='output.xmt_txt', model_name='MODEL_1')
```

---

## Undo / Redo

```python
Adams.undo_begin_block()   # start grouping commands into one undo step
# ... operations ...
Adams.undo_end_block()     # end the undo block

Adams.undo()    # reverse last undo block
Adams.redo()    # re-apply last undone block
```

---

## Model Verification

```python
m.verify()    # runs Adams View's built-in model topology checks
```

---

## Defaults — Units and Coordinate System

```python
d = Adams.defaults

# Units (set before building model)
d.units.length    = 'mm'
d.units.mass      = 'kg'
d.units.time      = 'second'
d.units.force     = 'newton'
d.units.angle     = 'degrees'
d.units.frequency = 'hz'

# Coordinate system (affects where markers/parts are placed without explicit location)
d.coordinate_system = some_part_or_marker   # place relative to this
d.coordinate_system = m.ground_part         # restore to global

# Get current active model
d.model    # Model — the currently active model
```

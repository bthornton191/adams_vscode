# file analysis read

Allows you to read a set of analysis files, which is a set of output files that Adams Solver generates during a simulation. The files include:

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `file_name` | String | Specifies the name of the file or files to be read. |
| `model_name` | New Model | Enter the model name under which you want to store the analysis files in the modeling database. |
| `analysis_name` | New or Existing Analysis | Specifies the name of the analysis in which to store output files. |
| `length(optional)` | mm, cm, meter, km, inch, foot, mile. | Specifies the length units in the file, if different from the current default. |
| `force(optional)` | newton, knewton, dyne, pound_force, kpound_force, kg_force, ounce_force, millinewton, centinewton, poundal. | Specifies the force units in the file, if different from the current default. |
| `mass(optional)` | kg, gram, pound_mass, kpound_mass, slug, ounce_mass, and tonne. | Specifies the mass units in the file, if different from the current default. |
| `time(optional)` | millisecond, second, minute, and hour. | Specifies the time units in the file, if different from the current default. |

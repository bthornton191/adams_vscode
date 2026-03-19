# part modify flexible_body auto_disable_modes

After performing a pilot simulation, you can disable those modes that do not significantly contribute to the total strain energy of a flexible body. You can set Adams View to automatically disable any modes that contributed less than a specified fraction of the total strain energy during the test simulation. After disabling the modes that do not significantly contribute to strain energy, simulation times should be reduced.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `flexible_body_name` | Existing flex body | Specifies the name of an existing flexible body to be modified |
| `energy_tolerance` | Real | Specifies a real number greater than 0 and less than 1. |
| `analysis_name` | Existing analysis | Specifies an existing analysis |

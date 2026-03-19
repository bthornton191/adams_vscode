# panel set acf_twindow eigen_solution_calculation

Specifies that you want Adams linearize the model about an operating point by performing an eigen solution analysis.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `damping` | Yes/No | Specifies if damping is to be included in the eigen solution analysis |
| `no_eigen_vectors` | True | Specifying the NO_EIGEN_VECTORS parameter indicates to Adams that the eigen solution analysis is to be performed without computation of mode shapes (eigenvectors). Only the eigenvalues will be reported. |
| `coordinates_of_modes` | Integer | This parameter is used to specify the mode numbers for which a table of mode shape coordinates will be output to the Adams output file. |
| `energy_of_modes` | Integer | This parameter is used to specify the mode numbers for which a table of modal energy distribution will be output to the Adams output file. |
| `dissipative_energy` | Integer | This parameter is used to specify the mode numbers for which a table of disspative energy distribution will be output to the Adams output file. |
| `kinetic_energy` | Integer | This parameter is used to specify the mode numbers for which a table of kinetic energy distribution will be output to the Adams output file. |
| `strain_energy` | Integer | This parameter is used to specify the mode numbers for which a table of strain energy distribution will be output to the Adams output file. |

# output_control create femdata

Produces data files of component loads, deformations, stresses, or strains for input to subsequent finite element or fatigue life analysis for use in third party products. Adams View will not output to any files unless you specify the format.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `femdata_name` | String | Specifies the name of the FEMDATA element in the modeling database to be created. |
| `adams_id` | Integer | Specifies an integer used to identify this element in the Adams data file. |
| `output_type` | loads/loads_on_flex/modal_deformation/stress/strain | Specifies the information you want as output: |
| `r_marker_name` | String | Specifies the rigid body marker to be the reference coordinate system to output loads. Because Adams Solver resolves all loads acting on the rigid body in the coordinate system of the specified marker, the marker should represent the FEA basic coordinate system of the part's finite element (FE) model. |
| `no_inertia` | yes/no | Specifies ‘yes’ for Adams View to include inertial loads (linear acceleration, angular acceleration, and velocity) when outputting the loads acting on the body. Otherwise, Adams View outputs no inertial loads and you will need to rely on an inertia relief capability in the finite element program to balance the external loads with the internal loads. |
| `peak_slice` | fx/fy/fz/fmag/gmag/tx/ty/tz/tmag/none/all | Specifies that FE model load data are to be output only at those time steps where the specified peak load occurred in the simulation. When you set the Time options, Adams View only checks the time steps within those specifications for the peak load. |
| `flex_body` | String | Enters the flexible body whose data Adams View outputs. Adams View outputs the data in the FE model basic coordinate system that is inherent to the flexible body. |
| `datum` | Integer | Enters the node ID of the flexible body to be the datum of the nodal displacements. |
| `nodes` | Integer | Enters the node numbers of a flexible body whose data is to be output. |
| `hotspots` | Integer | Enters the number of hot spots to locate and output. With this option, a text file containing a tab-delimited table of hot spot information, such as node ID, maximum value, time when the maximum value occurred, and location, is generated. |
| `radius` | Real | Enter a radius that defines the spherical extent of each hotspot. A default value of 0.0 (zero) means that all nodes in the flexible body will be hotspot candidates. |
| `criterion` | von_mises/max_principle/min_principle/max_shear/normal_x/normal_y/normal_z/shear_xy/shear_yz,shear_xz | Specifies the value of stress/strain in determining hotspots from one of Von Mises, Max Prin., Min Prin., Max Shear, Normal-X, Normal-Y, Normal-Z, Shear-XY, Shear-YZ, or Shear-ZX. |
| `file_name` | String | Enters the output file name for the FE model data. You can specify an existing directory, root name, and/or extension. By default, the file name will be composed of the Adams run and body IDs according to the type of data and file format that you specified in Solver -> Settings -> Output -> More -> Durability Files |
| `start` | Real | Specifies the time at which to start outputting the data. The default is the start of the simulation. |
| `end` | Real | Specifies the time at which to end the output of the data or the search of a peak load. The default is to output to the end of the simulation. |
| `skip` | Integer | Integer |

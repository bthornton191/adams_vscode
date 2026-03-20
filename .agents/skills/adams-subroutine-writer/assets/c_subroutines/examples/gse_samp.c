#include "slv_c_utils.h"

adams_c_Gsesample Gse_sample;
/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Gse_sample(const struct sAdamsGSE* gse, double time, int iflag, double* sample_step)
{
   *sample_step = 1.0e-3;
}

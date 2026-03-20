#include "slv_c_utils.h"

adams_c_Sevsub    Sevsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Sevsub(const struct sAdamsSensor* sensor, double time, int iflag, double* value)
{
/*
  Assign parameter values to readable variable names
*/
  int im = (int)sensor->PAR[0];
  int jm = (int)sensor->PAR[1];
  int ipar[3] = {im, jm, im};
  int errflg;
/*
      Call C_SYSFNC to collect state information
*/
  c_sysfnc("FY", ipar, 3, value, &errflg);
/*
  --- Check C_SYFNC call through C_ERRMES utility routine
*/
   c_errmes(errflg, "Error calling SYSFNC for FY", sensor->ID, "STOP");
}

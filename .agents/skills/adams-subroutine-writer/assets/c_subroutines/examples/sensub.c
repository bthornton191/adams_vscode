#include "slv_c_utils.h"

adams_c_Sensub    Sensub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Sensub(const struct sAdamsSensor* sensor, double time, int iflag, double* value)
{
/*
  Assign parameter values to readable variables
*/
   double x0=sensor->PAR[0];
   double h0=sensor->PAR[1];
   double x1=sensor->PAR[2];
   double h1=sensor->PAR[3];
   int    errflg;
/*
  --- Evaluate sensor ---------------------------------
  Get zeroth order value of step function 
*/

   c_step(time, x0, h0, x1, h1, 0, value, &errflg);

/*
  Check call to STEP function with error message utility
*/

   c_errmes(errflg,"Error calling STEP from SENSUB.",sensor->ID,"STOP");

}

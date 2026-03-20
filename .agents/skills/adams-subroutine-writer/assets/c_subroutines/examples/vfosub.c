#include "slv_c_utils.h"

adams_c_Vfosub    Vfosub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Vfosub(const struct sAdamsVforce* vfo, double time, int dflag, int iflag, double* result)
{
/*  Assign readable variable names to passed parameters */
   double c=vfo->PAR[0];
   int    ipar[3]={(int)vfo->PAR[1], (int)vfo->PAR[2],(int)vfo->PAR[1]};
/*  Local variables  */
   double vel[3];
   int    nstates;
   int    errflg;

/* call SYSARY for translation velocities TVEL */ 
   c_sysary("TVEL", ipar, 3, vel, &nstates, &errflg);
   c_errmes(errflg, "Error calling SYSARY for TVEL", vfo->ID, "STOP");

/*  --- Evaluate VFORCE components ------------------------- */
 
   result[0] = -c * vel[0];
   result[2] = -c * vel[1];
   result[2] = -c * vel[2];

}

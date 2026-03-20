#include "slv_c_utils.h"

adams_c_Mfosub Mfosub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Mfosub(const struct sAdamsMforce* mforce, double time, int dflag, int iflag, 
            const double* modloads, int nmodes, int ncases, double* scale, int* lcase, 
	    double* loadvec)
{
   int errflg;

   *lcase=(int)mforce->PAR[0];

   errflg=(ncases < *lcase);
   c_errmes(errflg, "Trying to use an invalid load case.", mforce->ID, "STOP");

   *scale=mforce->PAR[1];
}

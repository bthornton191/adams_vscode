#include "slv_c_utils.h"

adams_c_Difsub    Difsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Difsub(const struct sAdamsDiff* diff, double time, int dflag, int iflag, double* value)
{
   double lamda, pressure, prsdot;
   int    ipar[1];
   int    errflg;
/*
 * Assign readable variable names to passed parameters
*/
   lamda= diff->PAR[0];

/*
 * Get DIF(ID) and check for error
*/
   ipar[0] = diff->ID;
   c_sysfnc("DIF", ipar, 1, &pressure, &errflg);
   if(errflg)
      c_errmes(errflg, "Error calling SYSFNC for DIF.", diff->ID, "STOP");
/*
 * Get DIF1(ID) and check for error
*/
   c_sysfnc("DIF1", ipar, 1, &prsdot, &errflg);
   if(errflg)
      c_errmes(errflg, "Error calling SYSFNC for DIF.", diff->ID, "STOP");
/*
 * Evaluate pressure error function
*/
   *value  = pressure - lamda * prsdot;
}



#include "slv_c_utils.h"
#include <stdio.h>

adams_c_Motsub    Motsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Motsub(const struct sAdamsMotion* motion, double time, int iord, int iflag, double* value)
{
 double shift=motion->PAR[0];
 double omega=motion->PAR[1];
 int    nmcoef=motion->NPAR-2;
 double coef[30];
 int    errflg;

 int i;
 for(i=0; i<nmcoef; i++)*(coef+i) = *(motion->PAR+i+2);

/*
   Obtain value by evaluating FORCOS
*/

  c_forcos(time, shift, omega, coef, nmcoef, iord, value, &errflg);

/*
  Check for errors...
*/
  if(errflg){
     char msg[50];
     sprintf(msg, "Error calling FORCOS from MOTSUB for order = %i", iord);
     c_errmes(errflg, msg, motion->ID, "STOP");
  }
}

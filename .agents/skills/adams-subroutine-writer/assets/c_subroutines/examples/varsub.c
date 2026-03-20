#include "slv_c_utils.h"

adams_c_Varsub    Varsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Varsub(const struct sAdamsVariable* variable, double time, int dflag, int iflag, double* value)
{
/* Load up marker arrays for calls to sysfnc  */
   int ilist[2]={(int)variable->PAR[0], (int)variable->PAR[1]};
   int mlist[3]={(int)variable->PAR[2], (int)variable->PAR[3],(int)variable->PAR[4]};
   int jlist[2]={(int)variable->PAR[2], (int)variable->PAR[3]};
   int klist[3]={(int)variable->PAR[5], (int)variable->PAR[6],(int)variable->PAR[7]};
/* local variables */
   double dz1, dz2, dx, accz;
   int    errflg;

/* Call sysfnc for DZ(1022, 2201) */
   c_sysfnc("DZ", ilist, 2, &dz1, &errflg);
   c_errmes(errflg, "Error getting DZ from VARSUB.",variable->ID,"STOP");

/* Call sysfnc for DZ(1224, 2341, 2341) */
   c_sysfnc("DZ", mlist, 3, &dz2, &errflg);
   c_errmes(errflg, "Error getting DZ from VARSUB.",variable->ID,"STOP");

/* Call sysfnc for DX(1224, 2341) */
   c_sysfnc("DX", jlist, 2, &dx, &errflg);
   c_errmes(errflg, "Error getting DZ from VARSUB.",variable->ID,"STOP");

/* Call sysfnc for ACCZ( 7654, 4567, 1022) */
   c_sysfnc("ACCZ", klist, 3, &accz, &errflg);
   c_errmes(errflg, "Error getting DZ from VARSUB.",variable->ID,"STOP");

/* Define current value of VARIABLE  */

   *value = dz1 - dz2 + dx + accz;
}

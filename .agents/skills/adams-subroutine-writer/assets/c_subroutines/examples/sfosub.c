#include "slv_c_utils.h"

adams_c_Sfosub    Sfosub;
/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Sfosub(const struct sAdamsSforce* sforce, double time, int dflag, int iflag, double* value)
{
/* Assign impact parameters to readable variable names */
   double implth = sforce->PAR[3];
   double stiff  = sforce->PAR[4];
   double expont = sforce->PAR[5];
   double cmax   = sforce->PAR[6];
   double cdepth = sforce->PAR[7];
/* Load up ipar for call to sysfnc for DZ( PAR(1), PAR(2), PAR(3) ) */
   int    ipar[3]={(int)sforce->PAR[0],(int)sforce->PAR[1], (int)sforce->PAR[2] };
   int    errflg;
   double impary[3];
   double dz;
   double vz;

/* Call SYSFNC for displacement */

   c_sysfnc("DZ", ipar, 3, &dz, &errflg);
   c_errmes(errflg, "Error getting disp. in SFOSUB.", sforce->ID, "STOP");
 
/* Call SYSFNC for velocity */
 
    c_sysfnc("VZ", ipar, 3, &vz, &errflg);
    c_errmes(errflg, "Error getting vel. in SFOSUB.", sforce->ID, "STOP");
/*
  --- Evaluate force ----------------------------------
 
  Calculate IMPACT force 
*/
    c_impact(dz, vz, implth, stiff, expont, cmax, cdepth, 0,  impary, &errflg );
    c_errmes(errflg, "Error in IMPACT from SFOSUB.", sforce->ID, "STOP");

/* Assign the returned value */
 
    *value = impary[0];
}

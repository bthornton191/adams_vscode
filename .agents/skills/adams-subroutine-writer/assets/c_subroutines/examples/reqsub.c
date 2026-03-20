#include "slv_c_utils.h"

adams_c_Reqsub    Reqsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Reqsub(const struct sAdamsRequest* req, double time, int iflag, double* output)
{
 int ipar[1]={(int)req->PAR[0]};
 double difval;
 double derval;
 int errflg;

/*
  --- Create request information ----------------------
 
  Get DIF(PAR(1)) and check for error
*/
   c_sysfnc("DIF", ipar, 1, &difval, &errflg);
   c_errmes(errflg, "Error calling SYSFNC for DIF.",req->ID, "STOP");

/*
  Get DIF1(PAR(1)) and check for error
*/
 
   c_sysfnc("DIF1", ipar, 1, &derval, &errflg);
   c_errmes(errflg, "Error calling SYSFNC for DIF1.",req->ID, "STOP");

/*
  Assign the returned result values 
*/
   output[0] = 0.0;
   output[1] = difval;
   output[2] = derval;
   output[3] = 0.0;
   output[4] = 0.0;
   output[5] = 0.0;
   output[6] = 0.0;
   output[7] = 0.0;
}

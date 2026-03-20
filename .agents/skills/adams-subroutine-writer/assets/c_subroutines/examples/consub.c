#include "slv_c_utils.h"

adams_c_Consub    Consub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Consub(const struct sAdamsControl* con)
{

/*
 * --- Initial static analysis -------------------------
 *
 *  Initial call to ANALYS (INIFLG=.TRUE.)
 *
*/ 
   int iniflg=1;
   int status;
   c_analys("STATIC", "STATIC_1", 0.0, 0.0, iniflg, &status);
/* 
 *  If error occurred on ANALYS call, issue message
*/
   if(status)
      c_errmes(status, "Error calling ANALYS for STATIC_1.",
               status, "STOP");
/*
 * --- Output static results ---------------------------
*/
   c_datout(&status);

/*
 * --- Change the mass of PART/1 -----------------------
*/
      c_modify("PART/1, MASS = 10", &status);

/*
 *--- Perform static analysis again -------------------
 *
 * Second call to ANALYS (INIFLG=.FALSE.)
*/
   iniflg=0;
   c_analys("STATIC", "STATIC_2", 0.0, 0.0, iniflg, &status);
/* 
 *  If error occurred on ANALYS call, issue message
*/
   if(status)
      c_errmes(status, "Error calling ANALYS for STATIC_1.",
               status, "STOP");
/*
 * --- Output static results ---------------------------
*/
   c_datout(&status);

}

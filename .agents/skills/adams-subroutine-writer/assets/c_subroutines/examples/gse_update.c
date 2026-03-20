#include "slv_c_utils.h"

adams_c_Gseupdate Gse_update;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Gse_update(const struct sAdamsGSE* gse, double time, int dflag, int iflag, int ns, double* XDplus1)
{
   static double  A[2][2]={ .367880, 0.0, -7.3576, .36788};
   static double  B[2][2]={-.00528480, 0.00063212, -.00063212, 0.0};
   double         xd[2],u[2]; 
   int   axd[1]= {(int)(*(gse->PAR+0))};
   int   au[1] = {(int)(*(gse->PAR+1))};
   int   nds, nu, leflag;
/*
 *+--------------------------------------------------------------------*
 * Make sure there are 2 states, as assumed here
 *+--------------------------------------------------------------------*
*/
  if(ns != 2)
    c_errmes (1, "Wrong number of discrete states in gse_update",
              gse->ID, "ERROR");
			      
/* Get GSE input/state information   */

   c_sysary ("ARRAY", axd, 1, xd, &nds, &leflag);
   if(leflag) 
    c_errmes (leflag, "Error calling SYSARY for Xd in gse_update",
              gse->ID, "ERROR");

   c_sysary ("ARRAY", au,  1, u,  &nu, &leflag);
   if(leflag) 
    c_errmes (leflag, "Error calling SYSARY for U in gse_update",
              gse->ID, "ERROR");

/* Evaluate:
   Xd+1 = A*Xd + B*U    
*/
   XDplus1[0] = A[0][0]*xd[0]+A[1][0]*xd[1] + 
                B[0][0]*u[0] +B[1][0]*u[1];
   XDplus1[1] = A[0][1]*xd[0]+A[1][1]*xd[1] + 
                B[0][1]*u[0] +B[1][1]*u[1];
}


#include "slv_c_utils.h"

adams_c_Gseoutput  Gse_output;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Gse_output(const struct sAdamsGSE* gse, double time, int dflag, int iflag, int no, double* y)
{
   double C[2]={1.0E3, 0.0};

   int   Ax[1] = {(int)(*(gse->PAR+0))};
   double x[2];
   int   ns, leflag, parflg;
   
   c_sysary ("ARRAY", Ax, 1, x, &ns, &leflag);
   if(leflag) 
      c_errmes (leflag, "Error calling SYSARY  in gse_output",
                gse->ID, "ERROR");

/*  Evaluate the function   */
   *y = *(C+0)*(*(x+0)) + *(C+1)*(*(x+1));

/*  Calculate and return the derivative information:   */
   c_adams_needs_partials(&parflg);
   if (parflg) c_syspar("ARRAY", Ax, 1, C, ns, &leflag);

}   

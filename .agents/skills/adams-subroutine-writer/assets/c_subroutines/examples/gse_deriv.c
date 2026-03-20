
#include "slv_c_utils.h"

adams_c_Gsederiv  Gse_deriv;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Gse_deriv(const struct sAdamsGSE* gse, double time, int dflag, int iflag, int ns, double* XDot)
{
   double  A[4]={-1.0e3, 0.0, -2.0e4, -1.0e3};
   double  B[4]={ 0.0,   1.0, -1.0,    0.0  };
   double  x[2], u[2]; 

   int Ax[1] = {(int)*(gse->PAR+0)};
   int Au[1] = {(int)*(gse->PAR+1)};
   int nss, nu, leflag, parflg;

/*  Get GSE input/state information  */
   c_sysary ("ARRAY", Ax, 1, x, &nss, &leflag);
   if(leflag) 
      c_errmes (leflag, "Error calling SYSARY for X in gse_deriv",
                gse->ID, "ERROR");

   c_sysary ("ARRAY", Au, 1, u, &nu,  &leflag);
   if(leflag) 
      c_errmes (leflag, "Error calling SYSARY for U in gse_deriv",
                gse->ID, "ERROR");

/* Xdot = A*X + B*U      */
   *(XDot+0)= (*(A+0))*x[0]+(*(A+2))*x[1] + 
              (*(B+0))*u[0]+(*(B+2))*u[1];
   *(XDot+1)= (*(A+1))*x[0]+(*(A+3))*x[1] + 
              (*(B+1))*u[0]+(*(B+3))*u[1];

/* If Adams is evaluating the Jacobian return partials */
   c_adams_needs_partials(&parflg);
   if(parflg){
      c_syspar("ARRAY", Ax, 1, A, nss*nss, &leflag);
      c_syspar("ARRAY", Au, 1, B, nss*nu , &leflag);
   }
}


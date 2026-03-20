#include <stdio.h>
#include "slv_c_utils.h"

adams_c_Cffsub    Cffsub;
/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Cffsub(const struct sAdamsContactFriction* fric, double time, const double* loci, const double* locj, 
            const double* x, const double* xdot, double nforce, double area, int dflag, int iflag, 
	    double* force )
{
   *(force+0)=0.;
   *(force+1)=0.;
   *(force+2)=0.;
   if(! iflag){
         double us = *(fric->PAR+0);
         double ud = *(fric->PAR+1);
         double vs = *(fric->PAR+2);
         double vd = *(fric->PAR+3);
         double x0 = -vs;
         double h0 =  -1;
         double x1 =  vs;
         double h1 =   1;
	 double temp1, temp2;
	 int errflg;
         c_step(*xdot, x0, h0, x1, h1, 0, &temp1, &errflg);
         c_errmes(errflg,"ERROR CALLING STEP",fric->contact.ID,"CHECK");
         x0 = vs;
         h0 = us;
         x1 = vd;
         h1 = ud;
         c_step(*xdot, x0, h0, x1, h1, 0, &temp2, &errflg);
         c_errmes(errflg,"ERROR CALLING STEP",fric->contact.ID,"CHECK");
         *(force+0) = -nforce*temp1*temp2;
    }

}

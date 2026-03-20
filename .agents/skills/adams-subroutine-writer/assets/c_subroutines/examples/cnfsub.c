#include <stdio.h>
#include "slv_c_utils.h"

adams_c_Cnfsub    Cnfsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Cnfsub(const struct sAdamsContactFriction* cnf, double time, const double* loci, const double* ni, 
            const double* locj, const double* nj, double gap, double gapdot, double gapdotdot, 
	    double area, int dflag, int iflag, double* force )
{
   *(force+0)=0.;
   *(force+1)=0.;
   *(force+2)=0.;
   if(! iflag){
         double K = *(cnf->PAR+0);
         double E = *(cnf->PAR+1);
         double C = *(cnf->PAR+2);
         double D = *(cnf->PAR+3);
	 int errflg;
         c_impact(gap, gapdot, 0.0, K, E, C, D, 0, force, &errflg);
         c_errmes(errflg,"ERROR CALLING IMPACT",cnf->contact.ID,"CHECK");
   }

}


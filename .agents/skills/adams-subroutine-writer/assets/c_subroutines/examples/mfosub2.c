#include "slv_c_utils.h"
#include <math.h>

#define MAXN 100
#define ZERO 0.0
#define ONE  1.0
#define TWO  2.0
#define PI   3.141592653589793

adams_c_Mfosub Mfosub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Mfosub(const struct sAdamsMforce* mforce, double time, int dflag, int iflag,
            const double* modloads, int nmodes, int ncases, double* scale, int* lcase,
	    double* loadvec)
{
   int    fbyid[1]={(int)mforce->PAR[0]};
   int    mnum[MAXN];
   double mfrq[MAXN];
   double qdot[MAXN];
   int    errflg;
   int    nq;
   int    i;

/* ...  GET MODE NUMBERS AND FREQUENCIES FOR ALL ACTIVE MODES */
   c_modinf(fbyid[0], mnum, mfrq, &errflg);
   c_errmes(errflg, "FAILED CALL TO MODINF", mforce->ID, "STOP");

/* ...  GET TIME DERIVATIVE OF MODAL COORDINDATES             */
   c_sysary("QDOT", fbyid, 1, qdot, &nq, &errflg);
   c_errmes(errflg, "FAILED CALL TO SYSARY", mforce->ID, "STOP");

/* ...  CASE MUST BE SET TO ZERO                              */
      
   lcase = 0;
 
/* ...  BUILD MODAL LOAD AND RETURN IN LOADVEC ARRAY          */
               
   for(i=0; i<6; i++) loadvec[i] = ZERO;

   for(i=0; i < nmodes; i++){
      double gmas = ONE;
      double gstf = pow((TWO*PI*mfrq[i]),2);
      loadvec[i+6] = -TWO*sqrt(gstf*gmas)*qdot[i];
   }
}

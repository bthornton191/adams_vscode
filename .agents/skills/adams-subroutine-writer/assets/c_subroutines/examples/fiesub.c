#include "slv_c_utils.h"
#include <math.h>

adams_c_Fiesub    Fiesub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Fiesub(const struct sAdamsField* fie, double time,
            double* disp, double* velo, int dflag ,int iflag,
            double* field, double* dfddis, double* dfdvel)
{

/*
   fie    sAdamsField structure:
               int ID    Identifier of calling FIELD statement
               int Nfie->PAR  Number of passed fie->PARameters
            double fie->PAR   Array of passed statement fie->PARameters
               int I     Field I Marker
               int J     Field I Marker
   time     Current time
   disp     Array of I with respect to J displacements
   velo     Array of I with respect to J velocities
   dflag    Differencing flag
   iflag    Initialization pass flag
   field    Array of field values 
   dfddis   displacement fie->PARtial derivatives
   dfdvel   Velocity fie->PARtial derivatives 
*/
  
/* --- Calculate field component forces ----------------*/
/* Note: No velocity effects */
 
/* X translation field force */
 
      field[0] = - fie->PAR[0] * pow(disp[0],3)
                 - fie->PAR[1] * pow(disp[1],3)
                 - fie->PAR[2] * pow(disp[2],3)
                 - fie->PAR[3] * pow(disp[3],3)
                 - fie->PAR[4] * pow(disp[4],3)
                 - fie->PAR[5] * pow(disp[5],3);
 
/* No Y translation field force */
 
      field[1] = 0.0;
 
/* Z translation field force */
 
      field[2] = - fie->PAR[6] * pow(disp[0],3)
                 - fie->PAR[7] * pow(disp[1],3)
                 - fie->PAR[8] * pow(disp[2],3)
                 - fie->PAR[9] * pow(disp[3],3)
                 - fie->PAR[10]* pow(disp[4],3)
                 - fie->PAR[11]* pow(disp[5],3);
 
/* --- Calculate field component torques --------------- */
 
/* Note: No velocity effects */
 
/*  No X rotational field torque */
 
      field[3] = 0.0;
 
/* Y rotational field torque */
 
      field[4] = - fie->PAR[12] * disp[0] - fie->PAR[13] * disp[1] 
                 - fie->PAR[14] * disp[2] - fie->PAR[15] * disp[3]
                 - fie->PAR[16] * disp[4] - fie->PAR[17] * disp[5];
 
/* No Z rotational field torque */
 
      field[5] = 0.0;
/* 
  --- Assign returned fie->PARtial derivatives with --------
      respect to disp if this is a differencing pass
*/ 
   if ( dflag ) {
 
/* Initialize all derivatives to zero. */
 
      int i,j;
      for( j=0; j<6; j++){
         for( i=0; i<6; i++){
            dfddis[j*6+i] = 0.0;
            dfdvel[j*6+i] = 0.0;
         }
      }
 
/* Assign displacement partials for X force */
 
        dfddis[0*6+0] = -3.0 * fie->PAR[0] * pow(disp[0],2);
        dfddis[1*6+0] = -3.0 * fie->PAR[1] * pow(disp[1],2);
        dfddis[2*6+0] = -3.0 * fie->PAR[2] * pow(disp[2],2);
        dfddis[3*6+0] = -3.0 * fie->PAR[3] * pow(disp[3],2);
        dfddis[4*6+0] = -3.0 * fie->PAR[4] * pow(disp[4],2);
        dfddis[5*6+0] = -3.0 * fie->PAR[5] * pow(disp[5],2);
 
/* No Y force displacement partials  */
 
/* Assign displacement partials for Z force */
 
        dfddis[0*6+2] = -3.0 * fie->PAR[6]  * pow(disp[0],2);
        dfddis[1*6+2] = -3.0 * fie->PAR[7]  * pow(disp[1],2);
        dfddis[2*6+2] = -3.0 * fie->PAR[8]  * pow(disp[2],2);
        dfddis[3*6+2] = -3.0 * fie->PAR[9]  * pow(disp[3],2);
        dfddis[4*6+2] = -3.0 * fie->PAR[10] * pow(disp[4],2);
        dfddis[5*6+2] = -3.0 * fie->PAR[11] * pow(disp[5],2);
 
/* No X torque displacement partials  */
 
/* Assign displacement partials for Y torque */
 
         dfddis[0*6+4] = -fie->PAR[12];
         dfddis[1*6+4] = -fie->PAR[13];
         dfddis[2*6+4] = -fie->PAR[14];
         dfddis[3*6+4] = -fie->PAR[15];
         dfddis[4*6+4] = -fie->PAR[16];
         dfddis[5*6+4] = -fie->PAR[17];
 
/* No Z torque displacement partials  */
 
/* --- There are no partial derivatives with respect to VELO.  --- */

   }
}

#include <math.h>
#include "slv_c_utils.h"

adams_c_Cursub Cursub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void  Cursub( const struct sAdamsCurve* crv, double alpha, int iord, int iflag, double *value)
{
/*
 *
 * --- External variable definitions -------------------
 *
 * crv->ID       Identifier of calling CURVE statement 
 * crv->PAR      Array containing passed parameters
 * crv->NPAR     Number of passed parameters
 * alpha         Curve parameter value
 * iord          Derivative order of value to be returned
 * iflag         Initialization pass flag
 * value         Derivative values of CURVE returned to ADAMS
 *
 * === Executable code =================================
 *
*/
   double twopi, pi, radius, pitch, ang, x, y, dang;
   pi = acos(-1.0);
   twopi = 2.0*pi;
/*
 * Assign parameters to readable variable names
*/
   radius = *(crv->PAR+0);
   pitch  = *(crv->PAR+1);
/*
 * Compute helix angle, in radians, as function
 * of ALPHA (height)
*/
   ang  = twopi * alpha / pitch;
/*
 * Compute X and Y coordinates
*/
   x = radius*cos(ang);
   y = radius*sin(ang);
   
   switch( iord ) {
      case 0: /* Compute values for the X, Y, and Z coordinates */
        value[0] = x;
        value[1] = y;
	value[2] = alpha;
	break;
     case 1:  /* Compute values for the X, Y, and Z first derivatives */
        dang = twopi/pitch;
        value[0] =-x*dang;
        value[1] = y*dang;
	value[2] = 1.0;
	break;
     case 2:  /* Compute values for the X, Y, and Z second derivatives */
        dang = twopi/pitch;
        value[0] =-x*dang*dang;
        value[1] =-y*dang*dang;
	value[2] = 0.0;
        break;
  }
}

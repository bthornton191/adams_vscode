#include "slv_c_utils.h"

/*
 *  Using a function typedef from slv_c_utils.h, please declare your
 *  user subroutine before defining it.  This will allow a compiler to
 *  perform type checking for your subroutine arguments.
 */
    
adams_c_Gfosub    Gfosub;
/*
 *  Define a subroutine named 'Gfosub'.  Any name is allowed,
 *  as long as it is mixed case and the name is specified in 
 *  the ADAMS input file using the ROUTINE= keyword.  
 * 
 *  Adams distinguishes between FORTRAN and C subroutines by looking
 *  up the function name in the library.  If it finds a mixed case 
 *  name then it assumes that the function is a C function.  Otherwise
 *  it assumes Fortran.
 */

void Gfosub(const struct sAdamsGforce* gfo, double time, int dflag, int iflag, double* result)
{
  double ct =      gfo->PAR[0];
  double cr =      gfo->PAR[1];
  int    im = (int)gfo->PAR[2];
  int    jm = (int)gfo->PAR[3];
  double vel[6];
  int    ipar[3]; 
  int    nstates;
  int    errflg;
  
/*
      Call SYSARY to collect information for the
      calculations below. Note: if IFLAG is true, this
      call is actually setting functional dependencies.
 
  --- Use VEL to get marker translational and rotational
      velocities
*/
  ipar[0] = im;
  ipar[1] = jm;
  ipar[2] = im;
  c_sysary("VEL", ipar, 3, vel, &nstates, &errflg);
/*
  --- Check SYSARY call through ERRMES utility routine
*/
  c_errmes(errflg,"Error calling SYSARY for VEL", gfo->ID, "STOP");
/*
  --- Evaluate GFORCE components -------------------------
*/
  result[0] = -ct*vel[0];
  result[1] = -ct*vel[1];
  result[2] = -ct*vel[2];
  result[3] = -ct*vel[3];
  result[4] = -ct*vel[4];
  result[5] = -ct*vel[5];
}

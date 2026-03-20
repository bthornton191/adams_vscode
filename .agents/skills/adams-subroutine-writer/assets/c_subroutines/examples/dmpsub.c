#include "slv_c_utils.h"

adams_c_Dmpsub Dmpsub;

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void Dmpsub(const struct sAdamsCratio* flex, double time, const double* freqs, 
            int nmode, double stepsize, double* cratios)
{
/*
 --------------------------------------------------------------------
    The purpose of this subroutine is to compute modal damping as
    a ratio of critical damping for each mode of a flexible body.
    This routine is called when user has specified CRATIO = USER(...)
 
    Possible strategies to modify the default behavior include:
 
      1) reading CRATIO values from an array
      2) setting CRATIO based on the natural frequency pr mode number
      3) setting CRATIO based on the current simulation time
      4) stabilize the integrator by setting CRATIO based on the step size
 
    Increasing the damping ratio for a mode has the effect of
    eliminating the dynamics of the mode while preserving the
    compliance.  One might therefore set high damping (CRATIO = 1.)
    on high frequency modes but low damping on lower frequency modes.
 
  INPUT:
      flex       structure:
                 struct sAdamsFlexBody FlexBody
		 int     NPAR
		 double* PARcontaining PAR, ID 
		 
      time       The current simulation time
      stepsize   The current integrator step size
      freq       A vector of natural frequencies in Hz.
      nmode      The total number of modes
 
  OUTPUT:
     cratios     A vector of modal damping ratios.
 
*/

  int i;
  for(i=0; i<nmode; i++){
     if     (freqs[i] < flex->PAR[1]) cratios[i]=flex->PAR[0];
     else if(freqs[i] < flex->PAR[3]) cratios[i]=flex->PAR[2];
     else                            cratios[i]=flex->PAR[4];
  }
}


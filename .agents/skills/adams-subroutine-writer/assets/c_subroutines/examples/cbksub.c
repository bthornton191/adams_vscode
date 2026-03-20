
#include <stdio.h>
#include "slv_c_utils.h"
#include "slv_cbksub.h"
#include "slv_cbksub_util.h"

/*
 *  Using a function typedef from slv_c_utils.h, please declare your
 *  user subroutine before defining it.  This will allow a compiler to
 *  perform type checking for your subroutine arguments.
 */
    
adams_c_Callback    Cbksub;
/*
 *  Define a subroutine named 'Cbksub'.  Any name is allowed,
 *  as long as it is mixed case and the name is specified in 
 *  the ADAMS input file using the ROUTINE= keyword.  
 * 
 *  Adams distinguishes between FORTRAN and C subroutines by looking
 *  up the function name in the library.  If it finds a mixed case 
 *  name then it assumes that the function is a C function.  Otherwise
 *  it assumes Fortran.
 */

void Cbksub(const struct sAdamsCbksub *cbk, double time, int event, int *data)
{
/*
      Call USRMES to output information.
      
      get_event_name() is a utility which retrieves Solver events
*/
   c_usrmes(1, get_event_name(event), 0, "info");

   return;
}

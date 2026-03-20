
#include <math.h>

#include "slv_c_utils.h"

adams_c_Sursub Sursub;

#define EPS      1.0e-05
#define EPS10    1.0e-10
#define TWOPI    6.28318530717958648;

/*  
 This function determines whether or not the point xyz is on the surface.
 It assumes the surface is a circle with a hole in the middle
*/
static int P_XYZ_Is_Outside_S(double xyz[3], const int* NPAR, const double *PAR, double bnd_xyz[3], double closest_uv[2])
{

/* Inputs:

   double    xyz      A test point that may be inside or outside the surface.
   double*   PAR      User Parameters

   Outputs:

   double    bnd_xyz  If xyz is inside the surface, then bnd_xyz == xyz. 
                      If xyz is outside the surface, then bnd_xyz is returned
                      as the closest point to xyz which is on the surface.

   double    closest_uv  If xyz is inside the surface, then closest_uv == {0,0}. 
                         If xyz is outside the surface, then closest_uv is returned
                         as the {u,v} corresponding to bnd_xyz.
*/

/* Local Variables:   */

   double Rmin, Rmax, distance, theta;

/*---------------------------------------------------------------------*
   PAR array specification:
    [0] = minimum value of ALPHA
    [1] = maximum value of ALPHA
    [2] = minimum value of BETA
    [3] = maximum value of BETA
    [4] = flag indicating of surface is closed in ALPHA
    [5] = flag indicating of surface is closed in BETA
 
 ----------------------------------------------------------------------*/

/* Initialize:   */

   bnd_xyz[0] = xyz[0];
   bnd_xyz[1] = xyz[1];
   bnd_xyz[2] = xyz[2];

   Rmin = PAR[0];
   Rmax = PAR[1];

   distance = sqrt(xyz[0]*xyz[0] + xyz[1]*xyz[1]);

   /* This is the case where we are on the surface */
   if ((distance >= (Rmin-EPS10)) && (distance <= (Rmax+EPS10))) 
      return 0;

   theta = atan2(xyz[1], xyz[0]);

   if (theta < 0.0) theta += TWOPI;

   if (distance <= Rmin)
   {
      /* Inside the hole.  Project point to edge of hole */

      bnd_xyz[0] = Rmin*cos(theta);
      bnd_xyz[1] = Rmin*sin(theta);

      closest_uv[0] = Rmin;
      closest_uv[1] = theta;
   }
   else if (distance >= Rmax)
   {
      /* Outside of circle.  Project point to edge of circle */

      bnd_xyz[0] = Rmax*cos(theta);
      bnd_xyz[1] = Rmax*sin(theta);

      closest_uv[0] = Rmax;
      closest_uv[1] = theta;
   }

   return 1;
}


/*  
 This Sursub models a circle with a hole in the middle.  
*/
void Sursub(const struct sAdamsSurface* srf, double ALPHA, double BETA, 
            int IORD, int IFLAG, double* VALUES, int* IERR)
{
    
/* Inputs:

   const struct sAdamsSurface* srf pointer to the surface structure
   int       srf->ID     Identifier of calling SURFACE statement
   double*   srf->PAR    Array containing user parameters
   int       srf->NPAR   Number of user parameters
   double    ALPHA  alpha parameter of surface
   double    BETA   beta parameter of surface
   int       IORD   order of surface derivatives computed 
   int       IFLAG  Initial pass flag

   Outputs:

   double*    VALUES Array (dimension 3, 6, or 9, depending on order) 
                     of computed SURFACE components returned to ADAMS
   int*       IERR   ERROR flag.  0 indicates point is on surface
                                  1 indicates point is off surface
                     If point is off surface and IORD = 0, VALUES
                     should return the closest point which is on surface
*/

/* Local Variables:   */

   double RADIUS, THETA;

   double UV[2], BND_PT[3];


/*---------------------------------------------------------------------*
   PAR array specification:
    [0] = minimum value of ALPHA
    [1] = maximum value of ALPHA
    [2] = minimum value of BETA
    [3] = maximum value of BETA
    [4] = flag indicating of surface is closed in ALPHA
    [5] = flag indicating of surface is closed in BETA
 
 ----------------------------------------------------------------------*/

/* Initialize:   */

	VALUES[0] = 0.0;
	VALUES[1] = 0.0;
	VALUES[2] = 0.0;
	VALUES[3] = 0.0;
	VALUES[4] = 0.0;
	VALUES[5] = 0.0;
	VALUES[6] = 0.0;
	VALUES[7] = 0.0;
	VALUES[8] = 0.0;

   *IERR = 0;

   RADIUS = ALPHA;
   THETA  = BETA;

   if(IORD == 0)
   {
      /* Compute values for the X, Y, and Z coordinates

         VALUES[0] = X
         VALUES[1] = Y
         VALUES[2] = Z  */

      VALUES[0] = RADIUS*cos(THETA);
      VALUES[1] = RADIUS*sin(THETA);
      VALUES[2] = 0.0;
      
      VALUES[3] = ALPHA;
      VALUES[4] = BETA;

      if (P_XYZ_Is_Outside_S(VALUES, &srf->NPAR, srf->PAR, BND_PT, UV))
      {
         /* Point is off surface. Return the closest point on surface
            and (U,V) corresponding to the closest point  */

         *IERR = 1;

         VALUES[0] = BND_PT[0];
         VALUES[1] = BND_PT[1];
         VALUES[2] = 0.0;
         
         VALUES[3] = UV[0];
         VALUES[4] = UV[1];
      }
   }
   else if (IORD == 1)
   {
      /* Compute values for the first derivatives
         
      VALUES[0] = dX / dALPHA
      VALUES[1] = dY / dALPHA
      VALUES[2] = dZ / dALPHA
      VALUES[3] = dX / dBETA
      VALUES[4] = dY / dBETA
      VALUES[5] = dZ / dBETA  */

      VALUES[0] = cos(THETA);
      VALUES[1] = sin(THETA);
      VALUES[2] = 0.0;

      if (RADIUS < EPS)
      {
         VALUES[3] =-EPS*sin(THETA);
         VALUES[4] = EPS*cos(THETA);
      }
      else
      {
         VALUES[3] =-RADIUS*sin(THETA);
         VALUES[4] = RADIUS*cos(THETA);
      }
      
      VALUES[5] = 0.0;
   }
   else if (IORD == 2)
   {

      /* Compute values for the X, Y, and Z second derivatives

      VALUES[0] = d2X / dALPHA_dALPHA
      VALUES[1] = d2Y / dALPHA_dALPHA
      VALUES[2] = d2Z / dALPHA_dALPHA
      VALUES[3] = d2X / dALPHA_dBETA
      VALUES[4] = d2Y / dALPHA_dBETA
      VALUES[5] = d2Z / dALPHA_dBETA
      VALUES[6] = d2X / dBETA_dBETA
      VALUES[7] = d2Y / dBETA_dBETA
      VALUES[8] = d2Z / dBETA_dBETA   */

      VALUES[0] = 0.0;
      VALUES[1] = 0.0;
      VALUES[2] = 0.0;
      VALUES[3] =-sin(THETA);
      VALUES[4] = cos(THETA);
      VALUES[5] = 0.0;
      VALUES[6] =-RADIUS*cos(THETA);
      VALUES[7] =-RADIUS*sin(THETA);
      VALUES[8] = 0.0;
   }
   
   return;
}

/*
 **** Adams Solver  %W% %G%
 */

#include "slv_c_utils.h"
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <string.h>
#define BUF_LEN 256

adams_c_Spline_read Spline_read

/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

void sr_get_z_vals(FILE *fpr, int nvals, double z[]);
void sr_get_xy_vals(FILE *fpr, int nx, int nz, double x[], double y[]);


void Spline_read(const struct sAdamsSpline* spl, int *errflg)
{
/*
C
C***  This is an example user-written subroutine spline_read
C***  it reads spline data from a file if the format of the file
C***  has 1 comment line on top, then 1 line containing NX and NZ,
C***  then 1 line containing NZ Z values,
C***  then NX lines containing X, Y1, Y2, ... YNZ
C
C***  This lends itself to neat files for small values of NZ,
C***  but is not very useful for large values of NZ....
C
C***  This example uses formatted read statements.  Formatted reads
C***  are less likely to give platform dependent behavior.  The
C***  field widths used in the format specifications would need to be
C***  adjusted to match the data file format.  Alternatively, list
C***  directed (* format) read statements could be used.  List directed
C***  reads are more flexible wrt data format in the file, but may not
C***  perform the same on all platforms.
C
C+---------------------------------------------------------------------*
C
*/

char header[81];
int nx, nz;
FILE *fp;
double *z, *x, *y;

*errflg = 0;
if( (fp = fopen(spl->FILENAME,"r")) ) {           /* Open the data file */

   fgets(header, 80, fp );                    /* Read in header and check for format type */
   if(!strncmp(header,"ADAMSEXAMPLE",12)){

   fscanf( fp, "%d %d\n", &nx, &nz);         /* Read in size of date */

                                              /* Allocate Memory */
   x = (double*)malloc(nx*sizeof(double));
   y = (double*)malloc(nx*nz*sizeof(double));
   z = (double*)malloc(nz*sizeof(double));
  
   if( nz > 1 ) {                             /* Read Z values */
      sr_get_z_vals(fp, nz, z);
   }
     sr_get_xy_vals(fp, nx, nz, x, y);        /* Read X and Y values */

                                             /* Pass data to Adams */
   c_put_spline( spl->ID, nx, nz, x, y, z, errflg);
   c_errmes(*errflg, "Failed to put spline data", spl->ID, "STOP");
   
   free( x );                                 /* Release Memory */
   free( y );
   free( z );
   fclose( fp );                              /* Close File */
}
else {
*errflg = 1;
   c_errmes(*errflg, "Spline data file is of wrong format\n", spl->ID, "STOP");
}
}
else {
   *errflg = 0;
   c_errmes(*errflg, "Failed to open input file\0", spl->ID, "STOP");
}

}

void sr_get_z_vals(FILE *fpr, int nvals, double z[])
{
/* 
  The Z data is read off a single line.
*/
  char buf[BUF_LEN], *endpt;
  int  i;
  fgets(buf,BUF_LEN,fpr);
  endpt = buf;

  for(i=0;i <nvals;i++){
     z[i] = strtod(endpt, &endpt);
  }

}

void sr_get_xy_vals(FILE *fpr, int nx, int nz, double x[], double y[])
{
/* The Y data is stored as a set of column vectors by family.  
   y[0] = Y1Z1
   y[1] = Y2Z1
   y[2] = Y3Z1
   y[3] = Y4Z1
   .
   .
   .
   y[nx] = Y1Z2
   .
   .
   .
   y[nx*ny] = YnxZmz
*/

  char buf[BUF_LEN], *endpt;
  int  i,j;

  for(j=0;j < nx; j++){
    fgets(buf,BUF_LEN,fpr);
    endpt = buf;
    x[j] = strtod(endpt, &endpt);

    for(i=0;i <nz;i++){
      y[j + i*nx] = strtod(endpt, &endpt);
    }

  }

}


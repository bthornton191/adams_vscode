#ifndef SOLVER_C_UTILS_H
#define SOLVER_C_UTILS_H
/*
* Note:  
* Use mixed case names for the Adams subroutine names when using the C 
* style interface.  For the default subroutine name capitalize the first
* letter and have the remaining letters lower case; Gfosub for example. 
* Doing this insures that Adams Solver correctly distinguishes a C style 
* subroutine from Fortran and calls with the appropriate interface.
*  
*/

/* fortran calls */
#if (!defined LINKDLL_ASUTILITY)
#  if (defined _WIN32)
#   if (defined MAKE_ASUTILITY_DLL)
#     define LINKDLL_ASUTILITY __declspec(dllexport)
#   else
#     define LINKDLL_ASUTILITY __declspec(dllimport)
#   endif
#  else
#    define LINKDLL_ASUTILITY
#  endif
#endif

#if (!defined STDCALL)
#  ifdef _WIN32
#    define STDCALL __stdcall
#  else
#    define STDCALL
#  endif
#endif

#ifdef __cplusplus

// struct for Contact
struct sAdamsContactStiction
{
   sAdamsContactStiction() : b_stiction(0), n_incidents(1), max_stiction_deformation(0.01), max_angular_deformation(0.05) {}

   int    b_stiction;                // 0 = sliding,  1 = creeping
   int    n_incidents;               // number of incidents (incidents are added if n_incidents > 1)
   double max_stiction_deformation;  // max deformation in model length units
   double max_angular_deformation;   // max angular deformation in radians
};

/*
 *   CONTACT:  User defined geometry engine interface      ---------------------------------------
 */
typedef bool (*INITFUNC)    ( const char *units );
typedef bool (*TERMFUNC)    ( int partI, int partR );
typedef int  (*COLLIDEFUNC) ( const struct sAdamsContactStiction* stic, int body1, double *locI, double rotI[3][3], int body2, double *locR, double rotJ[3][3], int *nCpts );
typedef bool (*REPORTFUNC)  ( int index, double *ptI, double *nI, double *ptR, double *nR, double *contactArea, double *effectiveRadius, double *bbox );
typedef bool (*REPORTFREEFUNC)  ( int body1, int body2 );

/*
 *   CONTACT:  Utility function interface      ---------------------------------------
 */
typedef int  (*COLLIDESELFUNC) ( int body );
typedef bool (*REPORTSELFUNC)  ( int index, double *ptI, double *nI, double *ptR, double *nR, double *contactArea, double *effectiveRadius );
typedef bool (*REPORTFREESELFUNC)  ( int body );

typedef void (*PLUGINFUNC) (void);
typedef bool (*REPORTSMPFUNC) ( int body1, int body2, int index, double *ptI, double *nI, double *ptR, double *nR, double *contactArea, double *effectiveRadius, double *bbox);
typedef bool (*REPORTFLXFUNC) ( int body1, int body2, int index, int *numNodesI, int **nodeI, double **penI, int *numNodesR, int **nodeR, double **penR, int *nodesIFromTri, int *nodesJFromTri);
typedef bool (*GETTRIFUNC) ( int body1, int body2, int index, unsigned int *numTrisI, unsigned int **triI, unsigned int *numTrisJ, unsigned int **triJ );
typedef bool(*FINDTAGFUNC) (int tag);
typedef int (*SETPARAMFUNC) (const char *parameter, double *values);
typedef int (*GETPARAMFUNC) (const char *parameter, double *values);
typedef void (*FACETINGTOLERANCE)(double tol);
typedef double (*FFFUNC) ( int parentId, const double xdot, const double xdotdot, const double nForce);
typedef double (*USERFFFUNC) ( int parentId, const int nPar, const double *pPars, const double xdot, const double xdotdot, const double nForce);
typedef double (*DFFDGDOTFUNC) ( int parentId, const double xdot, const double xdotdot, const double dnForce );
typedef double (*DFFDTVFUNC) ( int parentId, const double xdot, const double xdotdot, const double nForce );
typedef double (*NFFUNC) ( int parentId, const double gap, const double gapdot, double gapdotdot);
typedef double (*DNFDGDOTFUNC) ( int parentId, const double gap, const double gapdot, double gapdotdot );
typedef double (*DTFUNC) (void);
typedef void (*CURVEFUNC)(int Id, void* Data, double alpha, int iOrd, double* Values);
typedef void (*SURFFUNC)(int Id, void* Data, double* alpha, int* iOrd, double* Values, int* iErr);
typedef bool (*THREADSAFEFUNC)(void);
typedef int (*CRBOXFUNC) (double diag[3]);
typedef int (*CRSPHFUNC) (double radius);
typedef int (*CRCYLFUNC) (double radius, double height, double angle, bool flipN);
typedef int (*CRELLFUNC) (double rx, double ry, double rz);
typedef int (*CRFRUFUNC) (double top_rad, double base_rad, double height, double angle, bool flipN);
typedef int (*CRTORFUNC) (double major_rad, double minor_rad, double angle);
typedef int (*CREXTFUNC) (const char *fileName, const char *partName, const char *elementName, int *errFlag);
typedef int (*CREXTFEPFUNC) (const char *fileName, const char *partName, const char *elementName, double beamLength, bool linear, int *errFlag);
typedef int (*CRSURFUNC) (const char *fileName, const char *partName, const char *elementName, const double *u_min, const double *u_max, const double *v_min, const double *v_max, const int *u_closed, const int *v_closed, int *errFlag);
typedef int (*CRTESFUNC) (int id, unsigned int numVert, unsigned int numFace, const double *vertices, const unsigned int *indices, int flexInfo, int *errFlag);
typedef int (*CRBTESFUNC) (int id, unsigned int numVert, unsigned int numFace, const double *vertices, const unsigned int *indices, int *errFlag);
typedef int (*VERTRIFUNC) (int tag, unsigned int TessellationAngle, unsigned int *numVerts, double* vertices, unsigned int *numTris, unsigned int* indices, int* error_code);
typedef int (*VERTRIBFUNC) (int tag, unsigned int TessellationAngle, unsigned int *numVerts, double* vertices, unsigned int *numTris, unsigned int* indices, double beamLength, bool isLinear, int* error_code);
typedef int (*GETVERFUNC) (int tag, unsigned int* numVerts, double** vertices, int* error_code);
typedef int (*SETVERFUNC) (int tag, unsigned int numVerts, const double* vertices, int* error_code);
typedef int (*SETVERBFUNC) (int tag, unsigned int numVerts, const double* vertices, double beamLength, bool linear, int* error_code);
typedef int (*OBBFUNC) (int tag, int* error_code);
typedef int (*MAXBBFUNC) (int tag, double* maxd, int* error_code);
typedef int (*CREXTRFUNC) (int tagG, int tagP);
typedef int (*CRREVFUNC) (int tagG, double angle);
typedef int (*CRSPLFUNC) (unsigned int order, unsigned int ncp, double* knot, double* cps, unsigned int pointSize, int closed);
typedef int (*CLIPGEOMFUNC) (int tag, unsigned int numVerts, const int* vert_list, const double* loop_normal, unsigned int* numTris, int* tri_list, int* error_code);
typedef int (*ADDTREEFUNC) (int tag, unsigned int numTris, const int* tri_list, int* error_code);

extern "C" 
{
 
/*
 *   Rendering structures for ANCF Beams    ----------------------------------------------------------
 */
struct sAdamsRenderNode
{
   double x, y, z;
   double psi, theta, phi;
};

}

/*
 -------------------------------------------------------------------------------
 CONTACT:  Beam Rendeing interface     
 -------------------------------------------------------------------------------
 See AdamsBeamRendering.h
*/
/* 
 static RenderingFE_PART* factoryCreate( int n_nodes, sAdamsRenderNode QG, sAdamsRenderNode *list_of_nodes, unsigned int fe_part_ID );
 */
typedef void* (*CREATEFEFUNC) (int n_nodes, sAdamsRenderNode QG, sAdamsRenderNode *list_of_nodes, unsigned int fe_part_id);
/* 
 void set_model_type(MODEL_TYPE type);
 */
typedef void* (*SETFEMODELFUNC) (void* pFE_Part, int model_type);
/* 
 void set_order_and_type( ORDER_TYPE ord = SECOND_ORDER, INTERPOLATION_TYPE itype = CONV_RATE_COMP );
*/
typedef void* (*SETFEBEAMTYPEFUNC) (void* pFE_Part, int order, int type);
/*
static void factoryDestroy( RenderingFE_PART *object );
*/
typedef void  (*DESTROYFEFUNC) (void* pFE_Part);
/*
static void factoryDestroyAll();
*/
typedef void  (*DESTROYALLFEFUNC) (void);
/*
beam_graphic* set_xyz_data( int n, double *p, int graphics_id );
*/
typedef void*  (*SETXYZFEFUNC) (void* pFE_Part, int n, double *p, int graphics_id);
/*
beam_graphic* set_xyz_data( int n, double *p, int graphics_id, double *rm );
*/
typedef void*  (*SETXYZRMFEFUNC) (void* pFE_Part, int n, double *p, int graphics_id, double *rm);
/*
beam_graphic* set_alphayz_data( int n, double *p, int graphics_id );
*/
typedef void*  (*SETALPHAYZFEFUNC) (void* pFE_Part, int n, double *p, int graphics_id);
/*
void set_triangle_data( int n, int *tri, int graphic_id ) 
*/
typedef void*  (*SETTRIFEFUNC) (void* pFE_Part, int n, unsigned int *pTri, int graphic_id);
/*
 void get_current( double *p, beam_graphic* graphic );
 */
typedef void  (*GETCURRENTXYZPFEFUNC) (void* pFE_Part, void* pFE_Graphic, double *p);
/*
 void get_current( double *p, beam_graphic* graphic, double *rm );
 */
typedef void  (*GETCURRENTXYZPRMFEFUNC) (void* pFE_Part, void* pFE_Graphic, double *p, double *rm);
/*
 void get_current( double *p, beam_graphic* graphic, double *rm );
 */
typedef void  (*GETNUMPOINTSFEFUNC) (void* pFE_Part, void* pFE_Graphic, unsigned int *n);
/*
 void out_put_alphayz_coordinates(double* p, const beam_graphic* grph);
 */
typedef void  (*GETALPHAYZPFEFUNC) (double *p, void* pFE_Part, void* pFE_Graphic);
/*
void set_q( double *q ) 
*/
typedef void  (*SETSTATESFEPARTFUNC) (void* pFE_Part, double *p);
/*
void set_q( int n, double *q ) 
*/
typedef void  (*SETSTATESFEFUNC) (void* pFE_Part, int n, double *p);
/*
static RenderingFE_PART* find( int fe_part_ID ); 
*/
typedef void* (*FINDPARTFEFUNC) (int fe_part_id);
/*
beam_graphic* search( int graphic_ID );
*/
typedef void* (*SEARCHGRAPHICFEFUNC) (void* pFE_Part, int graphic_id);
/*
void set_is_contact() 
*/
typedef void  (*SETCONTACTFEFUNC) (void* pFE_Part, void *bg);
/*
bool render_ok
*/
typedef bool (*CHECKFEPARTREADYFORRENDER) (void* pFE_Part);

/*
void update_all_graphics( int type ) 
*/
typedef void  (*UPDATEALLGRAPHICS) (int type);
/*
void go_back_to_initial() 
*/
typedef void  (*SETSTATESBACKTOINITIAL) (void* pFE_Part);

/*
void go_back_to_undeformed()
*/
typedef void  (*SETSTATESBACKTOUNDEFORMED) (void* pFE_Part);

/*
void get_s( double *nodes, int nn, double *s )
*/
typedef void  (*GETS4INTNODES) ( double *nodes, int nn, double *s );
/*
void XYZ_to_syz_in_beam( double* syz, const int N, const double* XYZ, const int nn, const double* nodes );
*/
/*
typedef void  (*GETSYZFUNC) ( double* syz, int N, double* XYZ, int nn, double* nodes );
*/
typedef void  (*GETSYZFUNC) ( double* syz, const int N, const double* XYZ, const int nn, const double* nodes );
/*
double mass_and_inertias( double *I, double *r_c, 
                          const int nn, double* nodes, const double rho,
                          const double* A, const double* Iyy, const double* Izz);
*/
typedef void  (*GETBEAMMASSINERTIA)(double* mass, double* I, double* mass_center,
         int number_of_nodes, double* Nodes, double rho, double* A, double* Iyy, double* Izz);
/*
bool verification_of_two_dimensional_beams(const int n_node, const double* nodes, const int axis, const double pos_tolerance);
*/
typedef void  (*VERIFYTWODIMFEPART)(bool* true_or_false, int number_of_nodes, double* Nodes, int axis, double tolerance);

// Not used by A/View
typedef void  (*CLEARGRAPHICFEFUNC) (void* pFE_Part, void* pFE_Graphic);
typedef void  (*CLEARALLGRAPHICFEFUNC) (void);
typedef void  (*SETBEAMFORMULATION) (void* pFE_Part, int order, int int_type );
typedef void* (*CREATEFEFUNCFROMSOLVER) (int n_nodes, double* L, int fe_part_id);
typedef void  (*GETSFUNC) (double* Nodes, int number_of_elements, double* s_int);
typedef unsigned int* (*GETTRIFEFUNC) (void* pFE_Part, void* pFE_Graphic, int *n);
#endif


#ifdef __cplusplus
extern "C" {
#endif
 
/*
 * Structures for c user subroutines
 */
struct sAdamsContact
{
   int ID;
   int nIGEOM;
   int nJGEOM;
   int* IGEOM;
   int* JGEOM;
   int* IFLIP_GEOM;
   int* JFLIP_GEOM;
};

struct sAdamsContactFriction
{
   struct sAdamsContact contact;
   int NPAR;
   const double* PAR;
};

/*
 *   CONTROL        ------------------------------------------------------------------------------
 */
struct sAdamsControl
{
   int NPAR;
   const double* PAR;
};

/*
 *   COUPLER        ------------------------------------------------------------------------------
 */
struct sAdamsCoupler
{
   int ID;
   int NPAR;
   const double* PAR;
   int NJOINT;
   int JOINTS[3];
   char TYPE[3];
};

/*
 *   CURVE          ------------------------------------------------------------------------------
 */
struct sAdamsCurve
{
   int ID;
   int NPAR;
   const double* PAR;
   int CLOSED;
   int ORDER;
   double MINPAR;
   double MAXPAR;
};

/*
 *   DIFF           ------------------------------------------------------------------------------
 */

struct sAdamsDiff
{
   int ID;
   int NPAR;
   const double* PAR;
   int STATIC_HOLD;
   int IMPLICIT;
   double IC_R1;
   double IC_R2;
};


/*
 *   FLEX_BODY      ------------------------------------------------------------------------------
 */
struct sAdamsFlexBody
{
   int ID;
   /* int NMAT;
   const int* MATRICES;
   int VM;
   int WM; */
};
struct sAdamsCratio
{
   struct sAdamsFlexBody FlexBody;
   int NPAR;
   const double* PAR;
};

/*
 *   FIELD          ------------------------------------------------------------------------------
 */
struct sAdamsField
{
   int ID;
   int NPAR;
   const double* PAR;
   int I;
   int J;
};

/*
 *   GFORCE         ------------------------------------------------------------------------------
 */
struct sAdamsGforce
{
   int ID;
   int NPAR;
   const double* PAR;
   int I;
   int RM;
   int JFLOAT;
};

/*
 *   GSE            ------------------------------------------------------------------------------
 */
struct sAdamsGSE
{
   int ID;
   int NPAR;
   const double* PAR;
   int NI;
   int NO;
   int U;
   int Y;
   int NS;
   int X;
   int IC;
   int STATIC_HOLD;
   int IMPLICIT;
   int STATICS_ONLY;
   int ND;
   int XD;
   int ICD;
   double SAMPLE_OFFSET;
};


/*
 *   EXTSYS         ------------------------------------------------------------------------------
 */
struct sAdamsEXTSYS
{
   int ID;
   int NPAR;
   const double* PAR;
   int NI;
   int NO;
   int U;
   int Y;
   int NS;
   int X;
   int IC;
   int STATIC_HOLD;
   int IMPLICIT;
   int ND;
   int XD;
   int ICD;
   double SAMPLE_OFFSET;
   const char* external_system_type;
   const char* model_file_name;
   int current_results_file_name_index;
   const char* output_file_name;
   const char* compute_resource;
   const char* memory_usage;
   int number_of_threads;
   int buffer_size;
   double memory_scale_factor;
   const char* scratch_file_directory;
};


/*
 *   MFORCE         ------------------------------------------------------------------------------
 */
struct sAdamsMforce
{
   struct sAdamsFlexBody FlexBody;
   int ID;
   int NPAR;
   const double* PAR;
   int JFLOAT;
};

/*
 *   MOTION         ------------------------------------------------------------------------------
 */

struct sAdamsMotion
{
   int ID;
   int NPAR;
   const double* PAR;
   int JOINT;
   const char* Type;
   int I;
   int J;
   char Which[2];
   const char* DVA;
};

/*
 *   REQUEST        ------------------------------------------------------------------------------
 */
struct sAdamsRequest
{
   int ID;
   int NPAR;
   const double* PAR;
   const char* COMMENT;
   const char* TITLE[8];
};

/*
 *   SENSOR         ------------------------------------------------------------------------------

struct sAdamsSensorEval
{
   int NPAR;
   const double* PAR;
};
*/
struct sAdamsSensor
{
   int ID;
   int NPAR;
   const double* PAR;
   double VALUE;
   double Error;
   char Logic[2];
   /* struct sAdamsSensorEval Eval; */
};

/*
 *   SFORCE         ------------------------------------------------------------------------------
 */
struct sAdamsSforce
{
   int ID;
   int NPAR;
   const double* PAR;
   int I;
   int J;
   int ACTION_ONLY;
   const char* Type;
};

/*
 *   SPLINE         ------------------------------------------------------------------------------
 */
struct sAdamsSpline
{
   int ID;
   const char* FILENAME;
   const char* BLOCKNAME;

};

/*
 *   SURFACE        ------------------------------------------------------------------------------
 */
struct sAdamsSurface
{
   int ID;
   int NPAR;
   const double* PAR;
   /* const char* FILENAME; */
   int ORDER[2];
   int CLOSED[2];
   double MINPAR[2];
   double MAXPAR[2];
};

/*
 *   VARIABLE       ------------------------------------------------------------------------------
 */
struct sAdamsVariable
{
   int ID;
   int NPAR;
   const double* PAR;
   double IC;
};

/*
 *   VFORCE         ------------------------------------------------------------------------------
 */
struct sAdamsVforce
{
   int ID;
   int NPAR;
   const double* PAR;
   int I;
   int JFLOAT;
   int RM;
};

/*
 *   VTORQUE        ------------------------------------------------------------------------------
 */
struct sAdamsVtorque
{
   int ID;
   int NPAR;
   const double* PAR;
   int I;
   int JFLOAT;
   int RM;
};

/*
*   CBKSUB        ------------------------------------------------------------------------------
*/
struct sAdamsCbksub
{
   int ID;
   int NPAR;
   const double* PAR;
   void *reserved;
};

/*
*   LINEAR        ------------------------------------------------------------------------------
*/
struct sAdamsLinearDataIn
{
   int  PINPUT;
   int  POUTPUT;
   int  PSTATE;
   int  RM;
   int  NODAMPIN;
   int  ORIGINAL;
   int  USEPBCS;
};

struct sAdamsLinearDataOut
{
   double *A;           // NS*NS
   double *B;           // NS*NI
   double *C;           // NO*NS
   double *D;           // NO*NI
   double *STATES;      // NS*1
   double *STATESINFO;  // NS*3
   int    NS;           // number of states
   int    NI;           // number of inputs
   int    NO;           // number of outputs
   int    ND;           // number of differential states
   int    NK;           // number of kinematic states
};

/*
 * End Structures
 */

/*
 *   CONTACT        ------------------------------------------------------------------------------
 */
typedef void adams_c_Cffsub(const struct sAdamsContactFriction* fric, double TIME, const double* LOCI, const double* LOCJ, const double* X, const double* XDOT, double NFORCE, double AREA, int DFLAG, int IFLAG, double* VALUES );
typedef void STDCALL adams_f77_CFFSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const double* LOCI, const double* LOCJ, const double* X, const double* XDOT, const double* NFORCE, const double* AREA, const int* DFLAG, const int* IFLAG, double* VALUES );

typedef void adams_c_Cnfsub(const struct sAdamsContactFriction* fric, double TIME, const double* LOCI, const double* NI, const double* LOCJ, const double* NJ, double GAP, double GAPDOT, double GAPDOTDOT, double AREA, int DFLAG, int IFLAG, double* VALUES );
typedef void STDCALL adams_f77_CNFSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const double* LOCI, const double* NI, const double* LOCJ, const double* NJ, const double* GAP, const double* GAPDOT, const double* GAPDOTDOT, const double* AREA, const int* DFLAG, const int* IFLAG, double* VALUES );
/*
 *   DIFF           ------------------------------------------------------------------------------
 */
typedef void adams_c_Difsub(const struct sAdamsDiff* diff, double TIME, int DFLAG, int IFLAG, double* RESULT);

typedef void STDCALL adams_f77_DIFSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, double* RESULT);
/*
 *   GFORCE         ------------------------------------------------------------------------------
 */
typedef void adams_c_Gfosub(const struct sAdamsGforce* gfo, double TIME, int DFLAG, int IFLAG, double* RESULT);
typedef void STDCALL adams_f77_GFOSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, double* RESULT);
/*
 *   MOTION         ------------------------------------------------------------------------------
 */
typedef void adams_c_Motsub(const struct sAdamsMotion* motion, double TIME, int IORD, int IFLAG, double* RESULT);

typedef void STDCALL adams_f77_MOTSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IORD, const int* IFLAG, double* RESULT);
/*
 *   SFORCE         ------------------------------------------------------------------------------
 */
typedef void adams_c_Sfosub(const struct sAdamsSforce* sforce, double TIME, int DFLAG, int IFLAG, double* RESULT);

typedef void STDCALL adams_f77_SFOSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, double* RESULT);
/*
 *   VARIABLE       ------------------------------------------------------------------------------
 */
typedef void adams_c_Varsub(const struct sAdamsVariable* variable, double TIME, int DFLAG, int IFLAG, double* RESULT);

typedef void STDCALL adams_f77_VARSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, double* RESULT);
/*
 *   VFORCE         ------------------------------------------------------------------------------
 */
typedef void adams_c_Vfosub(const struct sAdamsVforce* vfo, double TIME, int DFLAG, int IFLAG, double* RESULT);
typedef void STDCALL adams_f77_VFOSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, double* RESULT);
/*
 *   VTORQUE        ------------------------------------------------------------------------------
 */
typedef void adams_c_Vtosub(const struct sAdamsVtorque* vto, double TIME, int DFLAG, int IFLAG, double* RESULT);
typedef void STDCALL adams_f77_VTOSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, double* RESULT);
/*
 *   CURVE          ------------------------------------------------------------------------------
 */
typedef void adams_c_Cursub(const struct sAdamsCurve* crv, double ALPHA, int IORD, int IFLAG, double* VALUES  );
typedef void STDCALL adams_f77_CURSUB(const int* ID, const double* PAR, const int* NPAR, const double* ALPHA, const int* IORD, const int* IFLAG, double*  VALUES  );
/*
 *   SURFACE        ------------------------------------------------------------------------------
 */
typedef void adams_c_Sursub(const struct sAdamsSurface* srf, double ALPHA, double BETA, int IORD, int IFLAG, double* VALUES, int* IERR  );
typedef void STDCALL adams_f77_SURSUB(const int* ID, const double* PAR, const int* NPAR, const double* ALPHA, const double* BETA, const int* IORD, const int* IFLAG, double*  VALUES, int* IERR  );
/*
 *   REQUEST        ------------------------------------------------------------------------------
 */
typedef void adams_c_Reqsub(const struct sAdamsRequest* req, double TIME, int IFLAG, double* OUTPUT);
typedef void STDCALL adams_f77_REQSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, double* OUTPUT);
/*
 *   SENSOR         ------------------------------------------------------------------------------
 */
typedef void adams_c_Sensub(const struct sAdamsSensor* sensor, double TIME, int IFLAG, double* OUTPUT);
typedef void adams_c_Sevsub(const struct sAdamsSensor* sensor, double TIME, int IFLAG, double* OUTPUT);

typedef void STDCALL adams_f77_SENSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, double* OUTPUT);
typedef void STDCALL adams_f77_SEVSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, double* OUTPUT);
/*
 *   FIELD          ------------------------------------------------------------------------------
 */
typedef void adams_c_Fiesub(const struct sAdamsField* fie, double TIME, double* DISP, double* VELO, int DFLAG, int IFLAG,  double* FIELD, double* DFDDIS, double* DFDVEL);
typedef void STDCALL adams_f77_FIESUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const double* DISP, const double* VELO, const int* DFLAG, const int* IFLAG, double* FIELD, double* DFDDIS, double* DFDVEL);
/*
 *   CONTROL        ------------------------------------------------------------------------------
 */
typedef void adams_c_Consub(const struct sAdamsControl* con);
typedef void STDCALL adams_f77_CONSUB(const double* PAR, const int* NPAR);
/*
 *   COUPLER        ------------------------------------------------------------------------------
 */
typedef void adams_c_Cousub(const struct sAdamsCoupler* coupler, double TIME, double*, int IFLAG, double* PHI);
typedef void adams_c_Couxx(const struct sAdamsCoupler* coupler, double TIME, double*, int IFLAG, double* dFda);
typedef void adams_c_Couxx2(const struct sAdamsCoupler* coupler, double TIME, double*, int IFLAG, double* d2Fda2);
typedef void STDCALL adams_f77_COUSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, double* DISP, const int* NDISP, const int* IFLAG, double* F);
typedef void STDCALL adams_f77_COUXX(const int* ID, const double* TIME, const double* PAR, const int* NPAR, double* DISP, const int* NDISP, const int* IFLAG, double* dFda);
typedef void STDCALL adams_f77_COUXX2(const int* ID, const double* TIME, const double* PAR, const int* NPAR, double* DISP, const int* NDISP, const int* IFLAG, double* d2Fda2);
/*
 *   GSE            ------------------------------------------------------------------------------
 */
typedef void adams_c_Gsesub(const struct sAdamsGSE* gse, double TIME, int DFLAG, int IFLAG, int NSTATE, const double* STATES, int NINPUT, const double* INPUTS, int NPUTPUT, double* STATED, double* OUTPUT);
typedef void adams_c_Gsexu(const struct sAdamsGSE* gse, double TIME, int IFLAG, int NSTATE, const double* STATES, int NINPUT, const double* INPUTS, int NOUTPUTS, double* DERIVS);
typedef void adams_c_Gsexx(const struct sAdamsGSE* gse, double TIME, int IFLAG, int NSTATE, const double* STATES, int NINPUT, const double* INPUTS, int NOUTPUTS, double* DERIVS);
typedef void adams_c_Gseyu(const struct sAdamsGSE* gse, double TIME, int IFLAG, int NSTATE, const double* STATES, int NINPUT, const double* INPUTS, int NOUTPUTS, double* DERIVS);
typedef void adams_c_Gseyx(const struct sAdamsGSE* gse, double TIME, int IFLAG, int NSTATE, const double* STATES, int NINPUT, const double* INPUTS, int NOUTPUTS, double* DERIVS);
typedef void STDCALL adams_f77_GSESUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, const int* NSTATE, const double* STATES, const int* NINPUT, const double* INPUTS, const int* NOUTPUT, double* STATED, double* OUTPUT);
typedef void STDCALL adams_f77_GSEXU(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, const int* NSTATE, const double* STATES, const int* NINPUT, const double* INPUTS, const int* NOUTPUTS, double* DERIVS);
typedef void STDCALL adams_f77_GSEXX(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, const int* NSTATE, const double* STATES, const int* NINPUT, const double* INPUTS, const int* NOUTPUTS, double* DERIVS);
typedef void STDCALL adams_f77_GSEYU(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, const int* NSTATE, const double* STATES, const int* NINPUT, const double* INPUTS, const int* NOUTPUTS, double* DERIVS);
typedef void STDCALL adams_f77_GSEYX(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, const int* NSTATE, const double* STATES, const int* NINPUT, const double* INPUTS, const int* NOUTPUTS, double* DERIVS);

typedef void adams_c_Gsederiv(const struct sAdamsGSE* gse, double TIME, int DFLAG, int IFLAG, int, double*);
typedef void adams_c_Gseoutput(const struct sAdamsGSE* gse, double TIME, int DFLAG, int IFLAG, int, double*);
typedef void adams_c_Gseupdate(const struct sAdamsGSE* gse, double TIME, int DFLAG, int IFLAG, int, double*);
typedef void adams_c_Gsesample(const struct sAdamsGSE* gse, double TIME, int IFLAG, double* OUTPUT);

typedef void STDCALL adams_f77_GSEDERIV(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int*, const int*, const int*, double*);
typedef void STDCALL adams_f77_GSEOUTPUT(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int*, const int*, const int*, double*);
typedef void STDCALL adams_f77_GSEUPDATE(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int*, const int*, const int*, double*);
typedef void STDCALL adams_f77_GSESAMPLE(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, double* OUTPUT);

typedef void adams_c_Gsesetns(int NS, int* ERR);
typedef void adams_c_Gsesetnd(int ND, int* ERR);
typedef void adams_c_Gsesetimplicit(int FLAG, int* ERR);
typedef void adams_c_Gsesetstatichold(int FLAG, int* ERR);
typedef void adams_c_Gsesetsampleoffset(int UNTNUM, double* LOGERR);
typedef void adams_c_Gsesetstaticsonly(int FLAG, int* ERR);

typedef void STDCALL adams_f77_GSESETNS(int* NS, int* ERR);
typedef void STDCALL adams_f77_GSESETND(int* ND, int* ERR);
typedef void STDCALL adams_f77_GSESETIMPLICIT(int* FLAG, int* ERR);
typedef void STDCALL adams_f77_GSESETSTATICHOLD(int* FLAG, int* ERR);
typedef void STDCALL adams_f77_GSESETSAMPLEOFFSET(int* UNTNUM, double* LOGERR);
typedef void STDCALL adams_f77_GSESETSTATICSONLY(int* FLAG, int* ERR);

/*
 *   EXTSYS         ------------------------------------------------------------------------------
 */
typedef void adams_c_Extsysderiv(const struct sAdamsEXTSYS* extsys, double TIME, int DFLAG, int IFLAG, int, double*);
typedef void adams_c_Extsysoutput(const struct sAdamsEXTSYS* extsys, double TIME, int DFLAG, int IFLAG, int, double*);
typedef void adams_c_Extsysupdate(const struct sAdamsEXTSYS* extsys, double TIME, int DFLAG, int IFLAG, int, double*);
typedef void adams_c_Extsyssample(const struct sAdamsEXTSYS* extsys, double TIME, int IFLAG, double* OUTPUT);

typedef void STDCALL adams_f77_EXTSYSDERIV(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int*, const int*, const int*, double*);
typedef void STDCALL adams_f77_EXTSYSOUTPUT(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int*, const int*, const int*, double*);
typedef void STDCALL adams_f77_EXTSYSUPDATE(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int*, const int*, const int*, double*);
typedef void STDCALL adams_f77_EXTSYSSAMPLE(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* IFLAG, double* OUTPUT);

typedef void adams_c_Extsyssetns(int NS, int* ERR);
typedef void adams_c_Extsyssetnd(int ND, int* ERR);
typedef void adams_c_Extsyssetimplicit(int FLAG, int* ERR);
typedef void adams_c_Extsyssetstatichold(int FLAG, int* ERR);
typedef void adams_c_Extsyssetsampleoffset(int UNTNUM, double* LOGERR);

typedef void STDCALL adams_f77_EXTSYSSETNS(int* NS, int* ERR);
typedef void STDCALL adams_f77_EXTSYSSETND(int* ND, int* ERR);
typedef void STDCALL adams_f77_EXTSYSSETIMPLICIT(int* FLAG, int* ERR);
typedef void STDCALL adams_f77_EXTSYSSETSTATICHOLD(int* FLAG, int* ERR);
typedef void STDCALL adams_f77_EXTSYSSETSAMPLEOFFSET(int* UNTNUM, double* LOGERR);

typedef void adams_c_Extsyssetbodyinertia(const struct sAdamsEXTSYS* extsys,int swap_type, double* cm_xyz, double* im_xyz, double* im_dcm, double* mass, double* rot_inertia, int* n_nodes, double** nodes, int* n_modes, double** modes, double** gen_mass, double** gen_stiff, double** t_modes, double** r_modes, double** pre_load, double* cm_vel, double** modal_vel);
typedef void adams_c_Extsysseticsdva(const struct sAdamsEXTSYS* extsys, int analysis_type, int swap_type, double* d, double* v, double* acc, double* bcs_dcm, double* w, double* wdt, int nmodes, double* modal_q, double* modal_qdot, double* modal_qddot, int nmarkers, int* marker_nid, double* marker_force, double* x, double* xdot);
typedef void adams_c_Extsysrecoveroset(const struct sAdamsEXTSYS* extsys);
typedef void adams_c_Extsysoutputstepreq(const struct sAdamsEXTSYS* extsys, double time, int* file_name_index);
typedef void adams_c_Extsystimestepend(const struct sAdamsEXTSYS* extsys, double time);
typedef void adams_c_Extsysresultseparation(const struct sAdamsEXTSYS* extsys);
typedef void adams_c_Extsysgetgeometryinfo(const struct sAdamsEXTSYS* extsys, int* num_of_nodes, int* num_of_faces, int* face_list_size);
typedef void adams_c_Extsysgetface(const struct sAdamsEXTSYS* extsys, int* face_data);
typedef void adams_c_Extsysgetgeometry(const struct sAdamsEXTSYS* extsys, double* node_data);
typedef void adams_c_Extsyssetnodalforce(const struct sAdamsEXTSYS* extsys, int num_of_nodes, int* node_index, double* force_data);

/*
 *   CALLBACK       ------------------------------------------------------------------------------
 */
typedef void adams_c_Callback(const struct sAdamsCbksub *sos, double time, int type, int *mode);
typedef void STDCALL adams_f77_Callback(const double* time, const int *type, const int *mode);

/*
 *   FLEX_BODY      ------------------------------------------------------------------------------
 */
typedef void adams_c_Dmpsub(const struct sAdamsCratio* flex, double TIME, const double* FREQS, int NMODE, double STEPSIZE, double* CRATIOS);
typedef void STDCALL adams_f77_DMPSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const double* FREQS, const int* NMODE, const double* STEPSIZE, double* CRATIOS);
/*
 *   MFORCE         ------------------------------------------------------------------------------
 */
typedef void adams_c_Mfosub(const struct sAdamsMforce* mforce, double TIME, int DFLAG, int IFLAG, const double* MODLOADS, int NMODES, int NCASES, double* SCALE, int* CASE, double* LOADVEC);

typedef void STDCALL adams_f77_MFOSUB(const int* ID, const double* TIME, const double* PAR, const int* NPAR, const int* DFLAG, const int* IFLAG, const double* MODLOADS, const int* NMODS, const int* NCASES, double* SCALE, int* CASE, double* LOADVEC);
/*
 *   SAVE/RELOAD    ------------------------------------------------------------------------------
 */
typedef void adams_c_Relsub(int IUNIT, int* IERR);
typedef void adams_c_Savsub(int IUNIT, int* IERR);
typedef void STDCALL adams_f77_RELSUB(const int* IUNIT, int* IERR);
typedef void STDCALL adams_f77_SAVSUB(const int* IUNIT, int* IERR);
/*
 *   SPLINE         ------------------------------------------------------------------------------
 */
typedef void adams_c_Spline_read(const struct sAdamsSpline* spline, int* IERR);
#ifdef _WIN32
typedef void STDCALL adams_f77_SPLINE_READ(const int* ID, const char* FILENAME, int l_FILENAME, const char* BLOCKNAME, int l_BLOCKNAME, int* IERR);
#else
typedef void STDCALL adams_f77_SPLINE_READ(const int* ID, const char* FILENAME, const char* BLOCKNAME, int* IERR, int l_FILENAME, int l_BLOCKNAME);
#endif
/*
 *   USER MESSAGE FILTER ????         ------------------------------------------------------------
 */
/* USRMSGFLT. Only function to return an int */
typedef int adams_c_Usrmsgflt(char*, char*);
#ifdef _WIN32
typedef int STDCALL adams_f77_USRMSGFLT(char*, int, char*, int);
#else
typedef int STDCALL adams_f77_USRMSGFLT(char*, char*, int, int);
#endif


/*=================================================================================================
 *
 *   UTILITY SUBROUTINES
 *
 *=================================================================================================
 */

LINKDLL_ASUTILITY void c_adams_needs_partials(int *eval_jac);
LINKDLL_ASUTILITY void c_adams_declare_threadsafe();
LINKDLL_ASUTILITY void c_adams_smp_group(int groupid );

LINKDLL_ASUTILITY void c_set_partial_method(int method );


LINKDLL_ASUTILITY int c_gse_ns();
LINKDLL_ASUTILITY int c_gse_nd();
LINKDLL_ASUTILITY int c_gse_ni();
LINKDLL_ASUTILITY int c_gse_no();
LINKDLL_ASUTILITY void c_gse_x(double* x, int ns);
LINKDLL_ASUTILITY void c_gse_xd(double* xd, int nd);
LINKDLL_ASUTILITY void c_gse_xdot(double* xdot, int ndot);
LINKDLL_ASUTILITY void c_gse_u(double* u, int ni);
LINKDLL_ASUTILITY void c_gsepar_x(const double* par_x, int size);
LINKDLL_ASUTILITY void c_gsepar_xdot(const double* par_x, int size);
LINKDLL_ASUTILITY void c_gsepar_u(const double* par_u, int size);
LINKDLL_ASUTILITY void c_gsemap_x(int row, int col);
LINKDLL_ASUTILITY void c_gsemap_xdot(int row, int col);
LINKDLL_ASUTILITY void c_gsemap_u(int row, int col);

// 10JUNE2013. S. Riley. Return the number of active external systems in the model.
LINKDLL_ASUTILITY int c_extsys_nactive();

// 10JUNE2013. S. Riley. Return an array of the IDs of the active external systems in the model.
LINKDLL_ASUTILITY void c_extsys_ids_active(int* ids, int nactive);

LINKDLL_ASUTILITY int c_extsys_ns();
LINKDLL_ASUTILITY int c_extsys_nd();
LINKDLL_ASUTILITY int c_extsys_ni();
LINKDLL_ASUTILITY int c_extsys_no();
LINKDLL_ASUTILITY void c_extsys_set_x_ics(double* xics, const int ns);
LINKDLL_ASUTILITY void c_extsys_get_x_ics(double* xics, int ns);
LINKDLL_ASUTILITY void c_extsys_x(double* x, int ns);
LINKDLL_ASUTILITY void c_extsys_xd(double* xd, int nd);
LINKDLL_ASUTILITY void c_extsys_xdot(double* xdot, int ndot);
LINKDLL_ASUTILITY void c_extsys_u(double* u, int ni);
LINKDLL_ASUTILITY void c_extsys_newtimestep(double new_time_step);
LINKDLL_ASUTILITY void c_extsys_update_cputime(double my_cputime);
LINKDLL_ASUTILITY void c_extsys_corr_conv(int conv_flag, double LTE_sum);
LINKDLL_ASUTILITY void c_extsys_set_rebased_states(const double *x, const double *xdot, int ns);
LINKDLL_ASUTILITY void c_extsyspar_x(const double* par_x, int size);
LINKDLL_ASUTILITY void c_extsyspar_xdot(const double* par_x, int size);
LINKDLL_ASUTILITY void c_extsyspar_u(const double* par_u, int size);
LINKDLL_ASUTILITY void c_extsysmap_x(int row, int col);
LINKDLL_ASUTILITY void c_extsysmap_xdot(int row, int col);
LINKDLL_ASUTILITY void c_extsysmap_u(int row, int col);
LINKDLL_ASUTILITY void c_extsys_set_x_type(int index, int type);
LINKDLL_ASUTILITY int c_extsys_get_x_type(int index);
LINKDLL_ASUTILITY void c_extsys_marker(int id, int key, double x);
LINKDLL_ASUTILITY void c_extsyspar_marker_x(int id, int key, const double* par_x, int size);
LINKDLL_ASUTILITY void c_extsyspar_marker_xdot(int id, int key, const double* par_xdot, int size);
LINKDLL_ASUTILITY void c_extsyspar_marker_x2(int id, int key, const double* par_x2, int size);
LINKDLL_ASUTILITY void c_extsysmap_marker_x(int id, int key, int row);
LINKDLL_ASUTILITY void c_extsysmap_marker_xdot(int id, int key, int row);
LINKDLL_ASUTILITY void c_extsysmap_marker_x2(int id, int key, int row, int col);

LINKDLL_ASUTILITY void c_set_gse_state_tolerance(int gse_id, int index, double tol, int *ierr);
LINKDLL_ASUTILITY void c_get_solver_data(int type, void *in, void *out);
LINKDLL_ASUTILITY void c_get_thread_index(int *index);
LINKDLL_ASUTILITY void c_get_nthread(int *n);
LINKDLL_ASUTILITY void c_get_solver(int *n);
LINKDLL_ASUTILITY void c_gse_output_ics(int *n);
LINKDLL_ASUTILITY void c_set_dgse_type(int gse_id, int type);
LINKDLL_ASUTILITY double c_get_tinu();
LINKDLL_ASUTILITY void c_get_rt_process_mode(int *n);
LINKDLL_ASUTILITY void c_get_rt_end_of_warmup_period(double* t);
LINKDLL_ASUTILITY void c_get_numdif_info(int* numdif_int_info, double* numdif_float_info);

LINKDLL_ASUTILITY void c_get_integrator_details(int* integrator_type, int* corrector_type, double* delta_tolerance);
LINKDLL_ASUTILITY void c_get_HHT_parameters(double* alpha, double* beta, double* gamma);

LINKDLL_ASUTILITY void c_system_kinetic_energy(double* KE);
LINKDLL_ASUTILITY void c_system_momentum(int *iarg, double *linear, double *angular);
LINKDLL_ASUTILITY void c_body_mass_property(char *type, int *id, double *cm, double *mass, double *ip);
LINKDLL_ASUTILITY void c_add_mass_property(double *cm, double *mass, double *ip, double *sum_cm, double *sum_mass, double *sum_ip);
LINKDLL_ASUTILITY void c_subtract_mass_property(double *cm, double *mass, double *ip, double *sum_cm, double *sum_mass, double *sum_ip);

LINKDLL_ASUTILITY void c_akispl(double xval, double zval, int id, int iord, double *array, int *errflg);
LINKDLL_ASUTILITY void c_analys(const char *antype, const char *cid, double timbeg, double timend, int init, int *istat);
LINKDLL_ASUTILITY void c_bistop(double x, double dxdt, double x1, double x2,  double k, double e,
              double cmax, double d, int iord, double *vec, int *errflg);
LINKDLL_ASUTILITY void c_cheby(double x, double x0, const double *par, int npar, int iord, double *value, int *errflg);
LINKDLL_ASUTILITY void c_cubspl(double xval, double zval, int id, int iord, double *array, int *errflg);
LINKDLL_ASUTILITY void c_datout(int *istat);
LINKDLL_ASUTILITY void c_errmes(int errflg, const char *mesage, int id, const char *endflg);
LINKDLL_ASUTILITY void c_forcos(double x, double x0, double w,const double *par, int npar, int iord, double *value, int *errflg);
LINKDLL_ASUTILITY void c_forsin(double x, double x0, double w,const double *par, int npar, int iord, double *value, int *errflg);
LINKDLL_ASUTILITY void c_getcpu(double *value);
LINKDLL_ASUTILITY void c_get_gravity(double *gx, double* gy, double* gz);
LINKDLL_ASUTILITY void c_getinm(int *value);
LINKDLL_ASUTILITY void c_getint(char *value);
LINKDLL_ASUTILITY void c_getmod(int *mode);
LINKDLL_ASUTILITY void c_anlmod(int *mode);
LINKDLL_ASUTILITY void c_getslv(char *value);
LINKDLL_ASUTILITY void c_getstm(double *value);
LINKDLL_ASUTILITY void c_getver(char *value);
LINKDLL_ASUTILITY void c_gtaray(int id, double *array, int *number, int *istat);

LINKDLL_ASUTILITY void c_get_matrix_info(int id, int *type, int *nrows, int *ncols, int *size, int *ierr);
LINKDLL_ASUTILITY void c_get_sparse_matrix_data(int id, int* rows, int* cols, double* vals, int size, int* ierr);
LINKDLL_ASUTILITY void c_get_full_matrix_data(int id, double* vals, int size, int* ierr);


/* NOTE: For C the matrix c should be passed as a vector of
 *       minimum length = 36*nmid**2 and ndim = 6*nmid.
 *       The results will be returned column wise with
 *       iIndex = iRow + 6*iCol*nmid and c[iIndex] = c[iRow][iCol].
 */
LINKDLL_ASUTILITY void c_gtcmat(int nmid, const int *mid, int ndim, double *c, int *istat);
LINKDLL_ASUTILITY void c_gtcurv(int id, double alpha, int iord, double *array, int *istat);
LINKDLL_ASUTILITY void c_gtunts(int *exists, double *scales, char *units );
LINKDLL_ASUTILITY void c_gtstrg(int id, char *string, int *nchars, int *istat);
LINKDLL_ASUTILITY void c_havsin(double x, double x0, double h0, double x1, double h1, int iord,
              double *value, int *errflg);
LINKDLL_ASUTILITY void c_impact(double x, double dxdt, double x1, double k, double e, double cmax, double d,
              int iord, double *vec, int *errflg);
LINKDLL_ASUTILITY void c_istrng(int number, char *string, int *length, int *istat);
LINKDLL_ASUTILITY void c_modify(const char *comand, int *istat);
LINKDLL_ASUTILITY void c_nmodes(int id, int* nq, int* errflg);
LINKDLL_ASUTILITY void c_poly(double x, double x0, const double *par, int npar, int iord,
            double *value, int *errflg);
LINKDLL_ASUTILITY void c_put_spline(int id, int nxvals, int nzvals, const double *xvals, const double *yvals, const double *zvals, int *errflg);
LINKDLL_ASUTILITY void c_rcnvrt(const char *sys1, const double *coord1, const char *sys2, double *coord2, int *istat);
LINKDLL_ASUTILITY void c_rstrng(double reel, char *string, int *length, int *istat);
LINKDLL_ASUTILITY void c_shf(double x, double x0, double a, double w, double phi, double b, int iord,
           double *value, int *errflg);
LINKDLL_ASUTILITY void c_step(double x, double x0, double h0, double x1, double h1,
            int iord, double *value, int *errflg);
LINKDLL_ASUTILITY void c_step5(double x, double x0, double h0, double x1, double h1,
            int iord, double *value, int *errflg);
LINKDLL_ASUTILITY void c_sysary(const char *fncnam, const int *ipar, int nsize, double *states, int *nstate,
              int *errflg);
LINKDLL_ASUTILITY void c_sysfnc(const char *fncnam, const int *ipar, int nsize, double *states, int *errflg);
LINKDLL_ASUTILITY void c_sysfn2(const void *beam, const char *fncnam, const int *ipar, int nsize, int *index, int *errflg);
LINKDLL_ASUTILITY void c_naninf( const double *val, const int *size, int *outcome, int *index );
LINKDLL_ASUTILITY void c_syspar(const char *fncnam, const int *ipar, int nsize, const double *states, int nstate, int *errflg);
LINKDLL_ASUTILITY void c_tcnvrt(const char *sys1, const double *coord1, const char *sys2, double *coord2, int *istat);
LINKDLL_ASUTILITY void c_timget(double *time);
LINKDLL_ASUTILITY void c_tirary(int tireid, const char *fncnam, double *states, int *nstate, int *errflg);
LINKDLL_ASUTILITY void c_ucovar(int id, int nparts, const int *lparts, int nvars, const int *lvars);
LINKDLL_ASUTILITY void c_usrmes(int msgflg, const char *mesage, int id, const char *msgtyp);
/* Added by mnp */
LINKDLL_ASUTILITY void c_adams_serialize_integers(const int* data, int count);
LINKDLL_ASUTILITY void c_adams_unserialize_integers(int* data, int count);
LINKDLL_ASUTILITY void c_adams_serialize_doubles(const double* data, int count);
LINKDLL_ASUTILITY void c_adams_unserialize_doubles(double* data, int count);
LINKDLL_ASUTILITY void c_adams_serialize_characters(const char* data, int count);
LINKDLL_ASUTILITY void c_adams_unserialize_characters(char* data, int count);
LINKDLL_ASUTILITY void c_simsta(int* status);
LINKDLL_ASUTILITY void c_modinf(int id, int* mode, double* freq, int* errflg);
LINKDLL_ASUTILITY void c_setvelic(int object_id, int object_type,
                                  double* vm_ori, double* wm_loc, double* wm_ori,
                                  int nvics, double* vics, int* which, int* exact,
                                  int* errflg);
LINKDLL_ASUTILITY void c_realtime(const char *fncnam, int part_id, double *states, int *nstate, int *errflg);
LINKDLL_ASUTILITY void c_get_n_contact_incidents(int id, int *ninc, int *errflg);

LINKDLL_ASUTILITY void c_get_linear_mat_states(struct sAdamsLinearDataIn *in, struct sAdamsLinearDataOut *out, int *action);

#ifdef __cplusplus
// User-written subroutine for FE_LOAD
struct sAdamsANCF3DBeamDistrForce
{
   int ID;
   int NPAR;
   const double* PAR;
   double curr_S;
   double *mea_values;
   double* depend_Fx;
   double* depend_Fy;
   double* depend_Fz;
   double* depend_Tx;
   double* depend_Ty;
   double* depend_Tz;
   int type;
   void *beam;

   sAdamsANCF3DBeamDistrForce()
   {
      mea_values = 0;
      depend_Fx = depend_Fy = depend_Fz = depend_Tx = depend_Ty = depend_Tz = 0;
      ID = 0;
      NPAR = 0;
      PAR = 0;
      curr_S = 0;
      type = 0;
      beam = 0;
   }

   ~sAdamsANCF3DBeamDistrForce()
   {
      if (mea_values)
      {
         delete [] mea_values;        mea_values = 0;
      }
      if (depend_Fx)
      {
         delete [] depend_Fx;         depend_Fx = 0;
      }
      if (depend_Fy)
      {
         delete [] depend_Fy;         depend_Fy = 0;
      }
      if (depend_Fz)
      {
         delete [] depend_Fz;         depend_Fz = 0;
      }
      if (depend_Tx)
      {
         delete [] depend_Tx;         depend_Tx = 0;
      }
      if (depend_Ty)
      {
         delete [] depend_Ty;         depend_Ty = 0;
      }
      if (depend_Tz)
      {
         delete [] depend_Tz;         depend_Tz = 0;
      }
   }
};

/*
 *   ANCF Beams         ------------------------------------------------------------------------------
 */
typedef void adams_c_ANCFbeamsub( struct sAdamsANCF3DBeamDistrForce* sANCFbeam, double TIME, int DFLAG, int IFLAG, double* RESULT);


class AsFELOADSUB
{
public:
   static void pSYSFN2( const void *beam, const char* fname, const int* iarg, const int* narg, int *index, int* leflag, int len );
};
#endif

#ifdef __cplusplus
}
#endif


#endif


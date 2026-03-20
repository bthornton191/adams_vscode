#ifndef SLV_CBKSUB_H
#define SLV_CBKSUB_H

/*
   Enumerations used in the CBKSUB statement support.
*/

#ifdef __cplusplus
namespace CBKSUB {
#endif

typedef enum
{
   am_NULL = 0,
   am_KINEMATICS = 1,
   am_RESERVED = 2,
   am_INITIAL_CONDITIONS = 3,
   am_DYNAMICS = 4,
   am_STATICS = 5,
   am_QUASI_STATICS = 6,
   am_LINEAR = 7,
   am_STEADY_STATE = 8,
   am_COMPLIANCE = 9
}
ANALYSIS_MODE;

typedef enum
{
   ev_NOEVENT = 0,
   ev_INITIALIZE = 1,
   ev_TERMINATE = 2,
   ev_SENSOR = 3,      
   ev_ITERATION_BEG = 4,
   ev_ITERATION_END = 5,
   ev_BODY_ROTATION = 6,
   ev_OUTPUT_STEP_REQ = 7,
   ev_OUTPUT_STEP_BEG = 8,
   ev_OUTPUT_STEP_END = 9,
   ev_TIME_STEP_BEG = 10,
   ev_TIME_STEP_FAILED = 11,
   ev_TIME_STEP_END = 12,
   ev_MODEL_INPUT_BEG = 13,
   ev_MODEL_INPUT_END = 14,
   ev_DIS_IC_BEG = 15,
   ev_DIS_IC_END = 16,
   ev_VEL_IC_BEG = 17,
   ev_VEL_IC_END = 18,
   ev_ACC_IC_BEG = 19,
   ev_ACC_IC_END = 20,
   ev_STATICS_BEG = 21,
   ev_STATICS_END = 22,
   ev_STEADY_STATE_BEG = 23,
   ev_STEADY_STATE_END = 24,
   ev_KINEMATICS_BEG = 25,
   ev_KINEMATICS_END = 26,
   ev_DYNAMICS_BEG = 27,
   ev_DYNAMICS_END = 28,
   ev_LINEAR_BEG = 29,
   ev_LINEAR_END = 30,
   ev_QSTATICS_BEG = 31,
   ev_QSTATICS_END = 32,
   ev_SAVE_BEG = 33,
   ev_SAVE_END = 34,
   ev_RELOAD_BEG = 35,
   ev_RELOAD_END = 36,    
   ev_TRAN_SIM_BEG = 37,
   ev_TRAN_SIM_END = 38,
   ev_COMMAND = 39,
   ev_MODEL_CHANGE = 40,
   ev_FORCE_RECONC_BEG = 41,
   ev_FORCE_RECONC_END = 42,
   ev_PRIVATE_EVENT1 = 43,
   ev_PRIVATE_EVENT2 = 44,
   ev_LAST_EVENT = 45
}
EVENT_TYPE;

typedef enum
{
   cm_ACCGRAV = 1,
   cm_ACTIVATE = 2,
   cm_ARRAY = 3,
   cm_BEAM = 4,
   cm_BUSHING = 5,
   cm_CONTROL = 6,
   cm_COUPLER = 7,
   cm_CPAPAR = 8,
   cm_DEACTIVATE = 9,
   cm_DEBUG = 10,
   cm_DIFF = 11,
   cm_ENVIRONMENT = 12,
   cm_EQUILIBRIUM = 13,
   cm_FIELD = 14,
   cm_FILE = 15,
   cm_FLEX_BODY = 16,
   cm_FRICTION = 17,
   cm_GCON = 18,
   cm_GEAR = 19,
   cm_GFORCE = 20,
   cm_GSTIFF = 21,
   cm_HELP = 22,
   cm_HOTLINE = 23,
   cm_IC = 24,
   cm_INFO = 25,
   cm_INTEGRATOR = 26,
   cm_JOINT = 27,
   cm_JPRIM = 28,
   cm_KINEMATICS = 29,
   cm_LINEAR = 30,
   cm_LPARAM = 31,
   cm_LSOLVER = 32,
   cm_LTABLEPARAM = 33,
   cm_MARKER = 34,
   cm_MENU = 35,
   cm_MOTION = 36,
   cm_OUTPUT = 37,
   cm_PART = 38,
   cm_PREFERENCES = 39,
   cm_RELOAD = 40,
   cm_REQUEST = 41,
   cm_RETURN = 42,
   cm_SAVE = 43,
   cm_SENSOR = 44,
   cm_SFORCE = 45,
   cm_SHOW = 46,
   cm_SIMULATE = 47,
   cm_SPLINE = 48,
   cm_SPRINGDAMPER = 49,
   cm_STOP = 50,
   cm_STRING = 51,
   cm_TIME = 52,
   cm_VARIABLE = 53,
   cm_VFORCE = 54,
   cm_VTORQUE = 55,
   cm_WSTIFF = 56
}
COMMAND_IDENTIFIER;

typedef enum
{
   sn_CODGEN = 1,
   sn_DT = 2,
   sn_HALT = 3,
   sn_PRINT = 4,
   sn_RESTART = 5,
   sn_RETURN = 6,
   sn_STEPSIZE = 7,
   sn_YYDUMP = 8,
   sn_EVALUATE = 9
}
SENSOR_TYPE;

#ifdef __cplusplus
} // End of namespace CBKSUB
#endif

#endif

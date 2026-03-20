#ifndef SLV_CBKSUB_UTIL_H
#define SLV_CBKSUB_UTIL_H

#include "slv_cbksub.h"
/*
   Utilities for CBKSUB
*/

#ifdef __cplusplus
namespace CBKSUB {
#endif

char* get_simulation_analysis_mode( int m )
{
   switch( m )
   {
   case am_NULL: return "am_NULL";
   case am_KINEMATICS: return "am_KINEMATICS";
   case am_RESERVED: return "am_RESERVED";
   case am_INITIAL_CONDITIONS: return "am_INITIAL_CONDITIONS";
   case am_DYNAMICS: return "am_DYNAMICS";
   case am_STATICS: return "am_STATICS";
   case am_QUASI_STATICS: return "am_QUASI_STATICS";
   case am_LINEAR: return "am_LINEAR";
   case am_STEADY_STATE: return "am_STEADY_STATE";
   case am_COMPLIANCE: return "am_COMPLIANCE";
   default: return "UNKNOWNN_MODE";
   }
}

char* get_event_name( int ev )
{
   switch( ev )
   {
   case ev_NOEVENT: return "ev_NOEVENT";
   case ev_INITIALIZE: return "ev_INITIALIZE";
   case ev_TERMINATE: return "ev_TERMINATE";
   case ev_SENSOR : return "ev_SENSOR";
   case ev_ITERATION_BEG: return "ev_ITERATION_BEG";
   case ev_ITERATION_END: return "ev_ITERATION_END";
   case ev_BODY_ROTATION: return "ev_BODY_ROTATION";
   case ev_OUTPUT_STEP_REQ: return "ev_OUTPUT_STEP_REQ";
   case ev_OUTPUT_STEP_BEG: return "ev_OUTPUT_STEP_BEG";
   case ev_OUTPUT_STEP_END: return "ev_OUTPUT_STEP_END";
   case ev_TIME_STEP_BEG: return "ev_TIME_STEP_BEG";
   case ev_TIME_STEP_FAILED: return "ev_TIME_STEP_FAILED";
   case ev_TIME_STEP_END: return "ev_TIME_STEP_END";
   case ev_MODEL_INPUT_BEG: return "ev_MODEL_INPUT_BEG";
   case ev_MODEL_INPUT_END: return "ev_MODEL_INPUT_END";
   case ev_DIS_IC_BEG: return "ev_DIS_IC_BEG";
   case ev_DIS_IC_END: return "ev_DIS_IC_END";
   case ev_VEL_IC_BEG: return "ev_VEL_IC_BEG";
   case ev_VEL_IC_END: return "ev_VEL_IC_END";
   case ev_ACC_IC_BEG: return "ev_ACC_IC_BEG";
   case ev_ACC_IC_END: return "ev_ACC_IC_END";
   case ev_STATICS_BEG: return "ev_STATICS_BEG";
   case ev_STATICS_END: return "ev_STATICS_END";
   case ev_STEADY_STATE_BEG: return "ev_STEADY_STATE_BEG";
   case ev_STEADY_STATE_END: return "ev_STEADY_STATE_END";
   case ev_KINEMATICS_BEG: return "ev_KINEMATICS_BEG";
   case ev_KINEMATICS_END: return "ev_KINEMATICS_END";
   case ev_DYNAMICS_BEG: return "ev_DYNAMICS_BEG";
   case ev_DYNAMICS_END: return "ev_DYNAMICS_END";
   case ev_LINEAR_BEG: return "ev_LINEAR_BEG";
   case ev_LINEAR_END: return "ev_LINEAR_END";
   case ev_QSTATICS_BEG: return "ev_QSTATICS_BEG";
   case ev_QSTATICS_END: return "ev_QSTATICS_END";
   case ev_SAVE_BEG: return "ev_SAVE_BEG";
   case ev_SAVE_END: return "ev_SAVE_END";
   case ev_RELOAD_BEG: return "ev_RELOAD_BEG";
   case ev_RELOAD_END: return "ev_RELOAD_END";
   case ev_TRAN_SIM_BEG: return "ev_SIM_TRAN_BEG";
   case ev_TRAN_SIM_END: return "ev_SIM_TRAN_END";
   case ev_COMMAND: return "ev_COMMAND";
   case ev_MODEL_CHANGE: return "ev_MODEL_CHANGE";
   case ev_FORCE_RECONC_BEG: return "ev_FORCE_RECONC_BEG";
   case ev_FORCE_RECONC_END: return "ev_FORCE_RECONC_END";
   case ev_PRIVATE_EVENT1: return "ev_PRIVATE_EVENT1";
   case ev_PRIVATE_EVENT2: return "ev_PRIVATE_EVENT2";
   case ev_LAST_EVENT: return "ev_LAST_EVENT";
   default: return "UNKNOWN_EVENT";
   }
}

char* get_command_name( int c )
{
   switch( c )
   {
   case cm_ACCGRAV: return "cm_ACCGRAV";
   case cm_ACTIVATE: return "cm_ACTIVATE";
   case cm_ARRAY: return "cm_ARRAY";
   case cm_BEAM: return "cm_BEAM";
   case cm_BUSHING: return "cm_BUSHING";
   case cm_CONTROL: return "cm_CONTROL";
   case cm_COUPLER: return "cm_COUPLER";
   case cm_CPAPAR: return "cm_CPAPAR";
   case cm_DEACTIVATE: return "cm_DEACTIVATE";
   case cm_DEBUG: return "cm_DEBUG";
   case cm_DIFF: return "cm_DIFF";
   case cm_ENVIRONMENT: return "cm_ENVIRONMENT";
   case cm_EQUILIBRIUM: return "cm_EQUILIBRIUM";
   case cm_FIELD: return "cm_FIELD";
   case cm_FILE: return "cm_FILE";
   case cm_FLEX_BODY: return "cm_FLEX_BODY";
   case cm_FRICTION: return "cm_FRICTION";
   case cm_GCON: return "cm_GCON";
   case cm_GEAR: return "cm_GEAR";
   case cm_GFORCE: return "cm_GFORCE";
   case cm_GSTIFF: return "cm_GSTIFF";
   case cm_HELP: return "cm_HELP";
   case cm_HOTLINE: return "cm_HOTLINE";
   case cm_IC: return "cm_IC";
   case cm_INFO: return "cm_INFO";
   case cm_INTEGRATOR: return "cm_INTEGRATOR";
   case cm_JOINT: return "cm_JOINT";
   case cm_JPRIM: return "cm_JPRIM";
   case cm_KINEMATICS: return "cm_KINEMATICS";
   case cm_LINEAR: return "cm_LINEAR";
   case cm_LPARAM: return "cm_LPARAM";
   case cm_LSOLVER: return "cm_LSOLVER";
   case cm_LTABLEPARAM: return "cm_LTABLEPARAM";
   case cm_MARKER: return "cm_MARKER";
   case cm_MENU: return "cm_MENU";
   case cm_MOTION: return "cm_MOTION";
   case cm_OUTPUT: return "cm_OUTPUT";
   case cm_PART: return "cm_PART";
   case cm_PREFERENCES: return "cm_PREFERENCES";
   case cm_RELOAD: return "cm_RELOAD";
   case cm_REQUEST: return "cm_REQUEST";
   case cm_RETURN: return "cm_RETURN";
   case cm_SAVE: return "cm_SAVE";
   case cm_SENSOR: return "cm_SENSOR";
   case cm_SFORCE: return "cm_SFORCE";
   case cm_SHOW: return "cm_SHOW";
   case cm_SIMULATE: return "cm_SIMULATE";
   case cm_SPLINE: return "cm_SPLINE";
   case cm_SPRINGDAMPER: return "cm_SPRINGDAMPER";
   case cm_STOP: return "cm_STOP";
   case cm_STRING: return "cm_STRING";
   case cm_TIME: return "cm_TIME";
   case cm_VARIABLE: return "cm_VARIABLE";
   case cm_VFORCE: return "cm_VFORCE";
   case cm_VTORQUE: return "cm_VTORQUE";
   case cm_WSTIFF: return "cm_WSTIFF";
   default: return "UNKNOWN_COMMAND";
   }
}

char* get_sensor_type( int s )
{
   switch( s )
   {
   case sn_CODGEN: return "sn_CODGEN";
   case sn_DT: return "sn_DT";
   case sn_HALT: return "sn_HALT";
   case sn_PRINT: return "sn_PRINT";
   case sn_RESTART: return "sn_RESTART";
   case sn_RETURN: return "sn_RETURN";
   case sn_STEPSIZE: return "sn_STEPSIZE";
   case sn_YYDUMP: return "sn_YYDUMP";
   case sn_EVALUATE: return "sn_EVALUATE";
   default: return "UNKNOWN_SENSOR_TYPE";
   }
}

#ifdef __cplusplus
} // End of namespace CBKSUB
#endif

#endif

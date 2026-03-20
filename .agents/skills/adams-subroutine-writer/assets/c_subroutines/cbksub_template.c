/*
 * cbksub_template.c — Adams Solver CBKSUB skeleton (C)
 *
 * Build (using Adams mdi tool):
 *   First set up the build environment (once per session):
 *     python scripts/generate_adams_env.py
 *     call "%LOCALAPPDATA%\adams_env_init.bat"
 *   Then:
 *     Windows: mdi.bat cr-u n cbksub_template.c -n cbksub_template.dll ex
 *     Linux:   mdi -c cr-u n cbksub_template.c -n cbksub_template.so ex
 *
 * Adams dataset file (.adm):
 *   CBKSUB/1
 *   , USER(1.0)
 *   , ROUTINE=cbksub_template:Cbksub
 */

#include "slv_c_utils.h"      /* all structs, c_sysary, c_errmes, c_usrmes, etc. */
#include "slv_cbksub.h"       /* ev_*, am_*, cm_*, sn_* enums                     */
#include "slv_cbksub_util.h"  /* get_event_name() helper (optional)               */

/*
 * Forward declaration using the typedef from slv_c_utils.h.
 * This lets the compiler type-check the function signature below.
 */
adams_c_Callback  Cbksub;

/*
 * Global cache — add fields here for values you want to cache
 * from ev_ITERATION_BEG for use in other user subroutines.
 */
static struct {
    double cached_value;    /* example cached result */
    int    valid;           /* 1 = cache contains fresh data, 0 = stale */
} g_cache;

/**
 * @brief Called by Adams at each simulation lifecycle event.
 *
 * @param cbk   Pointer to element metadata (ID, NPAR, PAR[]); NULL on
 *              ev_INITIALIZE and ev_TERMINATE.
 *
 *      - cbk->ID      = CBKSUB element ID in the Adams model
 *      - cbk->NPAR    = number of USER() parameters
 *      - cbk->PAR[i]  = USER() parameter i (0-indexed)
 *
 * @param time  Current simulation time (seconds); undefined on ev_INITIALIZE.
 *
 * @param event Event identifier — always use ev_* named constants, never raw
 *              integers. Common values:
 *
 *      - ev_INITIALIZE      = one-time startup (cbk and time are undefined)
 *      - ev_TERMINATE       = one-time shutdown
 *      - ev_ITERATION_BEG   = start of each Newton iteration (primary cache point)
 *      - ev_ITERATION_END   = end of each Newton iteration
 *      - ev_STATICS_END     = after each static equilibrium solve
 *      - ev_SENSOR          = an Adams SENSOR element fired
 *      - ev_COMMAND         = an Adams command was issued
 *      - ev_PRIVATE_EVENT1  = internal solver event — MUST be ignored
 *      - ev_PRIVATE_EVENT2  = internal solver event — MUST be ignored
 *
 * @param data  Event payload array [3]; semantics depend on @p event:
 *
 *      ev_INITIALIZE / ev_TERMINATE:
 *      - data[0] = solver exit status (TERMINATE only)
 *
 *      ev_ITERATION_BEG / ev_ITERATION_END:
 *      - data[0] = simulation mode  (am_DYNAMICS, am_STATICS, am_KINEMATICS, ...)
 *      - data[1] = analysis mode    (am_*)
 *      - data[2] = 1 if a Jacobian/partial-derivative pass is required
 *
 *      ev_STATICS_END:
 *      - data[2] = 0 if converged, 1 if failed
 *
 *      ev_SENSOR:
 *      - data[0] = sensor element ID
 *      - data[1] = sensor action type (sn_HALT, sn_PRINT, ...)
 *
 *      ev_COMMAND:
 *      - data[0] = command identifier (cm_SIMULATE, cm_STOP, ...)
 *      - data[1] = 1 if issued from CONSUB, 0 otherwise
 *
 *      ev_PRIVATE_EVENT1 / ev_PRIVATE_EVENT2:
 *      - data[] MUST NOT be read — content is undefined
 */
void Cbksub( const struct sAdamsCbksub *cbk, double time, int event, int *data )
{
    /* Always invalidate cache at iteration boundary */
    g_cache.valid = 0;

    switch ( event )
    {
        case ev_INITIALIZE:  /* once before simulation; cbk and time are undefined */
            /* TODO: one-time initialization */
            break;

        case ev_TERMINATE:  /* once after simulation; data[0] = exit status */
            /* TODO: cleanup */
            break;

        case ev_ITERATION_BEG:  /* start of each Newton iteration — primary cache point */
        {
            int    ipar[3], nv, errflg;
            double states[6];

            /* Example: cache marker 16 displacement relative to marker 1
             * expressed in marker 1's frame.
             * Replace marker IDs and computation with your actual logic.
             */
            ipar[0] = 16;   /* moving marker ID */
            ipar[1] = 1;    /* reference marker ID */
            ipar[2] = 1;    /* result frame marker ID */
            errflg  = 0;

            c_sysary( "DISP", ipar, 3, states, &nv, &errflg );
            if ( errflg )
            {
                int id = cbk ? cbk->ID : 0;
                c_errmes( &errflg, "c_sysary DISP failed in Cbksub", &id, "STOP" );
                return;
            }

            g_cache.cached_value = -states[1] * 30.0;  /* example: Fy = -k*y */
            g_cache.valid        = 1;
            break;
        }

        case ev_STATICS_END:  /* after each static solve; data[2]=0 converged, 1 failed */
            if ( data[2] == 1 )
            {
                /* statics failed to converge — log or handle */
            }
            break;

        case ev_SENSOR:  /* data[0]=sensor ID, data[1]=action (sn_HALT, sn_PRINT, ...) */
            /* TODO: respond to sensor event if needed */
            break;

        case ev_COMMAND:  /* data[0]=command (cm_SIMULATE, cm_STOP, ...), data[1]=from CONSUB */
            if ( data[0] == cm_SIMULATE )
            {
                /* about to run a simulation */
            }
            break;

        case ev_PRIVATE_EVENT1:  /* internal solver events — MUST be ignored; never read data[] */
        case ev_PRIVATE_EVENT2:
            return;

        default:
            /* Ignore any events not handled above */
            break;
    }
}

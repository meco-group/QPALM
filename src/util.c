#include "util.h"
#include "lin_alg.h"
#include "global_opts.h"
#include <stdio.h>
/**********************
* Utility Functions  *
**********************/

void c_strcpy(char dest[], const char source[]) {
    int i = 0;

    while (1) {
        dest[i] = source[i];

        if (dest[i] == '\0') break;
        i++;
    }
}


QPALMSettings* copy_settings(QPALMSettings *settings) {
    QPALMSettings *new = c_malloc(sizeof(QPALMSettings));

    // Copy settings
    new->max_iter     = settings->max_iter;     
    new->eps_abs      = settings->eps_abs;       
    new->eps_rel      = settings->eps_rel;       
    new->eps_abs_in   = settings->eps_abs_in;    
    new->eps_rel_in   = settings->eps_rel_in;    
    new->rho          = settings->rho;           
    new->eps_prim_inf = settings->eps_prim_inf;  
    new->eps_dual_inf = settings->eps_dual_inf; 
    new->theta        = settings->theta;         
    new->delta        = settings->delta;
    new->tau_init     = settings->tau_init;         
    new->memory       = settings->memory; 
    new->proximal     = settings->proximal;       
    new->gamma        = settings->gamma;         
    new->gamma_upd    = settings->gamma_upd;     
    new->gamma_max    = settings->gamma_max;     
    new->scaling      = settings->scaling;      
    new->verbose      = settings->verbose;       

    return new;
}


void update_status(QPALMInfo *info, c_int status_val) {
    // Update status value
    info->status_val = status_val;

    // Update status string depending on status val
    if (status_val == QPALM_SOLVED) c_strcpy(info->status, "solved");

    else if (status_val == QPALM_PRIMAL_INFEASIBLE) c_strcpy(info->status,
                                                            "primal infeasible");
    else if (status_val == QPALM_UNSOLVED) c_strcpy(info->status, "unsolved");
    else if (status_val == QPALM_DUAL_INFEASIBLE) c_strcpy(info->status,
                                                            "dual infeasible");
    else if (status_val == QPALM_MAX_ITER_REACHED) c_strcpy(info->status,
                                                            "maximum iterations reached");
    else if (status_val == QPALM_NON_CVX) c_strcpy(info->status, "problem non convex");

}


void cold_start(QPALMWorkspace *work) {
    vec_set_scalar(work->x, 0., work->data->n);
    vec_set_scalar(work->x_prev, 0., work->data->n);
    vec_set_scalar(work->x0, 0., work->data->n);
    vec_set_scalar(work->y, 0., work->data->m);
    vec_set_scalar(work->Qx, 0., work->data->n);
    vec_set_scalar(work->Ax, 0., work->data->m);
}


void initialize_sigma(QPALMWorkspace *work) {
    c_float f = 0.5*vec_prod(work->x, work->Qx, work->data->n) + vec_prod(work->data->q, work->x, work->data->n);
    vec_ew_mid_vec(work->Ax, work->data->bmin, work->data->bmax, work->temp_m, work->data->m);
    vec_add_scaled(work->Ax, work->temp_m, work->temp_m, -1, work->data->m);
    c_float dist2 = vec_prod(work->temp_m, work->temp_m, work->data->m);
    vec_set_scalar(work->sigma, c_max(1e-8, c_min(2e1*c_max(1,c_absval(f))/c_max(1,0.5*dist2),1e8)), work->data->m);
}

/*******************
* Timer Functions *
*******************/

#ifdef PROFILING

// Windows
# ifdef _WIN32

void qpalm_tic(QPALMTimer *t)
{
  QueryPerformanceFrequency(&t->freq);
  QueryPerformanceCounter(&t->tic);
}

c_float qpalm_toc(QPALMTimer *t)
{
  QueryPerformanceCounter(&t->toc);
  return (t->toc.QuadPart - t->tic.QuadPart) / (c_float)t->freq.QuadPart;
}

// Mac
# elif defined __APPLE__

void qpalm_tic(QPALMTimer *t)
{
  /* read current clock cycles */
  t->tic = mach_absolute_time();
}

c_float qpalm_toc(QPALMTimer *t)
{
  uint64_t duration; /* elapsed time in clock cycles*/

  t->toc   = mach_absolute_time();
  duration = t->toc - t->tic;

  /*conversion from clock cycles to nanoseconds*/
  mach_timebase_info(&(t->tinfo));
  duration *= t->tinfo.numer;
  duration /= t->tinfo.denom;

  return (c_float)duration / 1e9;
}

// Mac
# elif defined __MACH__

void qpalm_tic(QPALMTimer *t)
{
  /* read current clock cycles */
  t->tic = mach_absolute_time();
}

c_float qpalm_toc(QPALMTimer *t)
{
  uint64_t duration; /* elapsed time in clock cycles*/

  t->toc   = mach_absolute_time();
  duration = t->toc - t->tic;

  /*conversion from clock cycles to nanoseconds*/
  mach_timebase_info(&(t->tinfo));
  duration *= t->tinfo.numer;
  duration /= t->tinfo.denom;

  return (c_float)duration / 1e9;
}

// Linux
# elif defined __linux__  /* ifdef _WIN32 */
/* read current time */

void qpalm_tic(QPALMTimer *t)
{
  clock_gettime(CLOCK_MONOTONIC, &t->tic);
}

/* return time passed since last call to tic on this timer */
c_float qpalm_toc(QPALMTimer *t)
{
  struct timespec temp;

  clock_gettime(CLOCK_MONOTONIC, &t->toc);

  if ((t->toc.tv_nsec - t->tic.tv_nsec) < 0) {
    temp.tv_sec  = t->toc.tv_sec - t->tic.tv_sec - 1;
    temp.tv_nsec = 1e9 + t->toc.tv_nsec - t->tic.tv_nsec;
  } else {
    temp.tv_sec  = t->toc.tv_sec - t->tic.tv_sec;
    temp.tv_nsec = t->toc.tv_nsec - t->tic.tv_nsec;
  }
  return (c_float)temp.tv_sec + (c_float)temp.tv_nsec / 1e9;
}

# endif /* ifdef IS_WINDOWS */

#endif // If Profiling end

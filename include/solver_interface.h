/**
 * @file solver_interface.h
 * @author Ben Hermans
 * @brief Interface and wrapper to matrix/factorization (ladel/cholmod) functions
 * @details This file includes all calls to cholmod/ladel functions apart from scaling in scaling.c and memory
 * allocation/deallocation in the main functions in qpalm.c. It includes all matrix operations, such as
 * matrix vector products, row- and columnwise norms, cholesky factorizations, factorization updates and
 * solving the linear system. Finally, all the settings relevant to cholmod (and suitesparse) are included
 * in this file as well.
 */

#ifndef SOLVER_INTERFACE_H
#define SOLVER_INTERFACE_H

# ifdef __cplusplus
extern "C" {
# endif // ifdef __cplusplus

#include "global_opts.h"
#include "constants.h"
#include "types.h"

/** 
 * Matrix-vector multiplication.
 *    
 * @f$y  =  A*x@f$
 * 
 * @param A Sparse matrix
 * @param x Dense input vector
 * @param y Dense output vector
 * @param c Solver environment 
 */
void mat_vec(solver_sparse *A,
             solver_dense  *x,
             solver_dense  *y,
             solver_common *c);
/** 
 * Matrix-transpose-vector multiplication.
 *    
 * @f$y  =  A^T*x@f$ 
 * 
 * @param A Sparse matrix
 * @param x Dense input vector
 * @param y Dense output vector
 * @param c Solver environment 
 */
void mat_tpose_vec(solver_sparse *A,
                   solver_dense  *x,
                   solver_dense  *y,
                   solver_common *c);

#ifdef USE_LADEL
#include "ladel_scale.h"
#define mat_inf_norm_cols ladel_infinity_norm_columns
#define mat_inf_norm_rows ladel_infinity_norm_rows
#elif defined USE_CHOLMOD
#include "cholmod.h"

/**
 * Infinity norm of each matrix column, @f$E_i = \|M{(:,i)}\|_\infty@f$.
 * 
 * @param M	Sparse input matrix
 * @param E Vector of infinity norms
 *
 */
void mat_inf_norm_cols(solver_sparse *M,
                       c_float   *E);

/**
 * Infinity norm of each matrix row, @f$E_i = \|M{(i,:)}\|_\infty@f$.
 * 
 * @param M	Sparse input matrix
 * @param E Vector of infinity norms
 *
 */
void mat_inf_norm_rows(solver_sparse *M,
                       c_float   *E);

/**
 * Calculate @f$LDL^T@f$ factorization of a matrix @f$M@f$.
 * 
 * If work->settings->proximal = true, use @f$M+\frac{1}{\gamma}*I@f$ instead.
 * 
 * @param M Matrix to be factorized
 * @param work Workspace
 * @param c Solver environment
 */
void ldlchol(solver_sparse *M, 
             QPALMWorkspace *work,
             solver_common *c);


/**
 * Calculate @f$LDL^T@f$ factorization of @f$Q+A{(a,:)}^T*\Sigma{(a,a)}*A{(a,:)}@f$, with @f$\Sigma=diag(\sigma)@f$ and @f$a@f$ the set of active constraints.
 * 
 * If work->settings->proximal = true, use @f$Q+\frac{1}{\gamma}*I+A{(a,:)}^T*\Sigma{(a,a)}*A{(a,:)}@f$ instead.
 * 
 * @param work Workspace
 * @param c Solver environment
 */
void ldlcholQAtsigmaA(QPALMWorkspace *work,
                      solver_common *c);

/**
 * Update the @f$LDL^T@f$ factorization given a set of entering constraints.
 * 
 * The index set of entering constraints is assumed to be set in work->solver->enter.
 * 
 * @param work Workspace
 * @param c Solver environment
 */
void ldlupdate_entering_constraints(QPALMWorkspace *work,
                                    solver_common *c);

/**
 * Downdate the @f$LDL^T@f$ factorization given a set of leaving constraints.
 * 
 * The index set of leaving constraints is assumed to be set in work->solver->leave.
 * 
 * @param work Workspace
 * @param c Solver environment
 */
void ldldowndate_leaving_constraints(QPALMWorkspace *work,
                                     solver_common *c);

/**
 * Update the @f$LDL^T@f$ factorization given a set of indexes where @f$sigma@f$ has been updated.
 * 
 * The index set of changed @f$sigma@f$ is assumed to be set in work->solver->enter.
 * 
 * @param work Workspace
 * @param c Solver environment
 */
void ldlupdate_sigma_changed(QPALMWorkspace *work,
                             solver_common *c);


/**
 * Solve the linear system @f$LDL^T*d = -\nabla \varphi@f$.
 * 
 * @param work Workspace
 * @param c Solver environment
 */
void ldlsolveLD_neg_dphi(QPALMWorkspace *work,
                         solver_common *c);

/**
 * Cholmod settings to indicate that we use an @f$LDL^T@f$ factorization.
 * 
 * In addition, this function sets the suitesparse memory allocation function to our custom functions.
 * 
 * @param c Solver environment
 */
void cholmod_set_settings(solver_common *c);

#endif /* USE_CHOLMOD */

# ifdef __cplusplus
}
# endif // ifdef __cplusplus

#endif // ifndef CHOLMOD_INTERFACE_H 
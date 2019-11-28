from ctypes import *
import platform
import numpy as np
import scipy as sc


class QPALMSettings(Structure):
    _fields_ = [("max_iter", c_long),
                ("inner_max_iter", c_long),
                ("eps_abs", c_double),
                ("eps_rel", c_double),
                ("eps_abs_in", c_double),
                ("eps_rel_in", c_double),
                ("rho", c_double),
                ("eps_prim_inf", c_double),
                ("eps_dual_inf", c_double),
                ("theta", c_double),
                ("delta", c_double),
                ("sigma_max", c_double),
                ("proximal", c_long),
                ("gamma_init", c_double),
                ("gamma_upd", c_double),
                ("gamma_max", c_double),
                ("scaling", c_long),
                ("nonconvex", c_long),
                ("verbose", c_long),
                ("print_iter", c_long),
                ("warm_start", c_long),
                ("reset_newton_iter", c_long),
                ("enable_dual_termination", c_long),
                ("dual_objective_limit", c_double),
                ("time_limit", c_double)
                ]

QPALMSettings_pointer = POINTER(QPALMSettings)

class cholmod_sparse(Structure):
    _fields_ = [("nrow", c_uint),
                ("ncol", c_uint),
                ("nzmax", c_uint),
                ("p", c_void_p),
                ("i", c_void_p),
                ("nz", c_void_p),
                ("x", c_void_p),
                ("z", c_void_p),
                ("stype", c_long),
                ("itype", c_long),
                ("xtype", c_long),
                ("dtype", c_long),
                ("sorted", c_long),
                ("packed", c_long)
                ]

cholmod_sparse_pointer = POINTER(cholmod_sparse)

class QPALMData(Structure):
    _fields_ = [("n", c_uint),
                ("m", c_uint),
                ("Q", cholmod_sparse_pointer),
                ("A", cholmod_sparse_pointer),
                ("q", POINTER(c_double)),
                ("c", c_double),
                ("bmin", POINTER(c_double)),
                ("bmax", POINTER(c_double))
                ]
QPALMData_pointer = POINTER(QPALMData)

# /**
#  * Solver return information
#  */
# typedef struct {
#   c_long   iter;           ///< number of iterations taken
#   c_long   iter_out;       ///< number of outer iterations (i.e. dual updates)
#   char    status[32];     ///< status string, e.g. 'solved'
#   c_long   status_val;     ///< status as c_long, defined in constants.h

#   c_float pri_res_norm;   ///< norm of primal residual
#   c_float dua_res_norm;   ///< norm of dual residual
#   c_float dua2_res_norm;  ///< norm of intermediate dual residual (minus proximal term)

#   c_float objective;      ///< objective function value
#   c_float dual_objective; ///< dual objective function value (= NaN if enable_dual_termination is false)

#   #ifdef PROFILING
#   c_float setup_time;    ///< time taken for setup phase (seconds)
#   c_float solve_time;    ///< time taken for solve phase (seconds)
#   c_float run_time;      ///< total time (seconds)
#   #endif

# } QPALMInfo;

class QPALMInfo(Structure):
    _fields_ = [("iter", c_long),
                ("iter_out", c_long),
                ("status", c_char*32),
                ("status_val", c_long),
                ("pri_res_norm", c_double),
                ("dua_res_norm", c_double),
                ("dua2_res_norm", c_double),
                ("objective", c_double),
                ("dual_objective", c_double),
                ("setup_time", c_double),
                ("solve_time", c_double),
                ("run_time", c_double)
                ]

QPALMInfo_pointer = POINTER(QPALMInfo)


# typedef struct array_element  {
#   c_float x; ///< value of the element
#   c_long   i; ///< index
# } array_element;

class array_element(Structure):
    _fields_ = [("x", c_double),
                ("i", c_long)]

class QPALMSolution(Structure):
    _fields_ = [("x", POINTER(c_double)),
                ("y", POINTER(c_double))]


class QPALMWork(Structure):
    _fields_ = [("data", QPALMData_pointer),
                ("x", POINTER(c_double)),
                ("y", POINTER(c_double)),
                ("Ax", POINTER(c_double)),
                ("Qx", POINTER(c_double)),
                ("Aty", POINTER(c_double)),
                ("x_prev", POINTER(c_double)),
                ("initialized", c_long),
                ("temp_m", POINTER(c_double)),
                ("temp_n", POINTER(c_double)),
                ("sigma", POINTER(c_double)),
                ("sqrt_sigma_max", c_double),
                ("nb_sigma_changed", c_long),
                ("gamma", c_double),
                ("gamma_maxed", c_long),
                ("Axys", POINTER(c_double)),
                ("z", POINTER(c_double)),
                ("pri_res", POINTER(c_double)),
                ("pri_res_in", POINTER(c_double)),
                ("yh", POINTER(c_double)),
                ("Atyh", POINTER(c_double)),
                ("df", POINTER(c_double)),
                ("x0", POINTER(c_double)),
                ("xx0", POINTER(c_double)),
                ("dphi", POINTER(c_double)),
                ("neg_dphi", POINTER(c_double)),
                ("dphi_prev", POINTER(c_double)),
                ("d", POINTER(c_double)),
                ("tau", c_double),
                ("Qd", POINTER(c_double)),
                ("Ad", POINTER(c_double)),
                ("sqrt_sigma", POINTER(c_double)),
                ("sqrt_delta", c_double),
                ("eta", c_double),
                ("beta", c_double),
                ("delta", POINTER(c_double)),
                ("alpha", POINTER(c_double)),
                ("temp_2m", POINTER(c_double)),
                ("delta2", POINTER(c_double)),
                ("delta_alpha", POINTER(c_double)),
                ("s", POINTER(array_element)),
                ("index_L", POINTER(c_long)),
                ("index_P", POINTER(c_long)),
                ("index_J", POINTER(c_long)),
                ("eps_pri", c_double),
                ("eps_dua", c_double),
                ("eps_dua_in", c_double),
                ("eps_abs_in", c_double),
                ("eps_rel_in", c_double),
                ("delta_y", POINTER(c_double)),
                ("Atdelta_y", POINTER(c_double)),
                ("delta_x", POINTER(c_double)),
                ("Qdelta_x", POINTER(c_double)),
                ("Adelta_x", POINTER(c_double)),
                ("D_temp", POINTER(c_double)),
                ("E_temp", POINTER(c_double)),
                ("chol", c_void_p),
                ("settings", QPALMSettings_pointer),
                ("scaling", c_void_p),
                ("solution", POINTER(QPALMSolution)),
                ("info", QPALMInfo_pointer),
                ("timer", c_void_p)
                ]

QPALMWork_pointer = POINTER(QPALMWork)

#   /** @} */

#   QPALMCholmod  *chol;     ///< cholmod variables
#   QPALMSettings *settings; ///< problem settings
#   QPALMScaling  *scaling;  ///< scaling vectors
#   QPALMSolution *solution; ///< problem solution
#   QPALMInfo     *info;     ///< solver information

#   # ifdef PROFILING
#   QPALMTimer *timer;       ///< timer object
#   # endif // ifdef PROFILING

# } QPALMWorkspace;



class Qpalm:
    """
    Wrapper class for the python interface to QPALM
    """
    def __init__(self):
        """
        Construct the wrapper class and load the dynamic library.
        """
        self._load_library()
        self._set_restypes()
        self._settings = self.python_interface.qpalm_malloc_settings()
        self.python_interface.qpalm_set_default_settings(self._settings)
    #def __del__(self):
        #self.python_interface.qpalm_cleanup(work)
    # def set_default_settings(self):
    #     self.python_interface.qpalm_set_default_settings(self._settings)
        
    def set_data(self, Q, A, q, bmin, bmax):
        """
        Convert the data to QPALMData structure.
        Parameters
        ---------
        Q : Quadratic part of the cost (scipy.csc_matrix)
        A : Constraint matrix (scipy.csc_matrix)
        q : Linear part of the cost (numpy.array)
        bmin : Lower bounds of the constraints (numpy.array)
        bmax : Upper bounds of the constraints (numpy.array)
        """
        self._data = self.python_interface.qpalm_malloc_data()
        
        (n,m) = Q.shape
        if n != m :
            print("ERROR: Q is not a square matrix")
        if len(q) != n :
            print("ERROR: q is not the right length")

        (m,nA) = A.shape 
        if m != 0 and n != nA :
            print("ERROR: A is not the right size")
        if len(bmin) != m :
            print("ERROR: bmin is not the right length")
        if len(bmax) != m :
            print("ERROR: bmax is not the right length")            

        c_double_p = POINTER(c_double)
        c_long_p = POINTER(c_long)

        self._data[0].n = n
        self._data[0].m = m
        self._data[0].q = q.ctypes.as_data(c_double_p)
        self._data[0].bmin = bmin.ctypes.as_data(c_double_p)
        self._data[0].bmax = bmax.ctypes.as_data(c_double_p)

        self._data[0].A[0].nrow = m
        self._data[0].A[0].ncol = n
        Ap = A.indptr
        Ai = A.indices
        self._data[0].A[0].p = Ap.ctypes.as_data(c_long_p)
        self._data[0].A[0].i = Ai.ctypes.as_data(c_long_p)
        self._data[0].A[0].nzmax = Ap[n]
        self._data[0].A[0].packed = 1
        self._data[0].A[0].sorted = 1
        self._data[0].A[0].nz = 0 #NULL
        self._data[0].A[0].itype = 2 #CHOLMOD_LONG 
        self._data[0].A[0].dtype = 0 #CHOLMOD_DOUBLE
        self._data[0].A[0].stype = 0 #Unsymmetric
        Ax = A.data
        self._data[0].A[0].x = Ax.ctypes.as_data(c_double_p)
        self._data[0].A[0].xtype = 1 #CHOLMOD_REAL

        self._data[0].Q[0].nrow = n
        self._data[0].Q[0].ncol = n
        Qp = Q.indptr
        Qi = Q.indices
        self._data[0].Q[0].p = Qp.ctypes.as_data(c_long_p)
        self._data[0].Q[0].i = Qi.ctypes.as_data(c_long_p)
        self._data[0].Q[0].nzmax = Qp[n]
        self._data[0].Q[0].packed = 1
        self._data[0].Q[0].sorted = 1
        self._data[0].Q[0].nz = 0 #NULL
        self._data[0].Q[0].itype = 2 #CHOLMOD_LONG 
        self._data[0].Q[0].dtype = 0 #CHOLMOD_DOUBLE
        self._data[0].Q[0].stype = -1 #Lower symmetric
        Qx = Q.data
        self._data[0].Q[0].x = Qx.ctypes.as_data(c_double_p)
        self._data[0].Q[0].xtype = 1 #CHOLMOD_REAL

    # def _allocate_work(self):

        # work = self.python_interface.qpalm_setup()


    def _load_library(self):
        """
        Load the dynamic QPALM library.
        """
        try:
            if (platform.system() == 'Linux'):
                print("OS is Linux")      
                self.python_interface = CDLL("../../build/lib/" + "libqpalm.so")
            elif (platform.system() == 'Windows'):
                print("OS is Windows")
            elif (platform.system() == 'Darwin'):
                print("OS is MacOS")
            else:
                print("ERROR: could not detect OS, using Linux")
        except:
            print("Failed to load dynamic library")

    def _set_restypes(self):
        """
        Set the return types for the relavent interface functions.
        """
        self.python_interface.qpalm_malloc_settings.restype = QPALMSettings_pointer
        self.python_interface.qpalm_malloc_data.restype = QPALMData_pointer
        self.python_interface.qpalm_setup.restype = QPALMWork_pointer

if __name__== '__main__':
    qpalm = Qpalm()
    # print("Default settings")
    # print("max_iter " + str(qpalm._settings.contents.max_iter))
    # print("inner_max_iter " + str(qpalm._settings.contents.inner_max_iter))
    # print("eps_abs " + str(qpalm._settings.contents.eps_abs))
    # print("eps_rel " + str(qpalm._settings.contents.eps_rel))
    # print("eps_abs_in " + str(qpalm._settings.contents.eps_abs_in))
    # print("eps_rel_in " + str(qpalm._settings.contents.eps_rel_in))
    # print("rho " + str(qpalm._settings.contents.rho))
    # print("eps_prim_inf " + str(qpalm._settings.contents.eps_prim_inf))
    # print("eps_dual_inf " + str(qpalm._settings.contents.eps_dual_inf))
    # print("theta " + str(qpalm._settings.contents.theta))
    # print("delta " + str(qpalm._settings.contents.delta))
    # print("sigma_max " + str(qpalm._settings.contents.sigma_max))
    # print("proximal " + str(qpalm._settings.contents.proximal))
    # print("gamma_init " + str(qpalm._settings.contents.gamma_init))
    # print("gamma_upd " + str(qpalm._settings.contents.gamma_upd))
    # print("gamma_max " + str(qpalm._settings.contents.gamma_max))
    # print("scaling " + str(qpalm._settings.contents.scaling))
    # print("nonconvex " + str(qpalm._settings.contents.nonconvex))
    # print("verbose " + str(qpalm._settings.contents.verbose))
    # print("print_iter " + str(qpalm._settings.contents.print_iter))
    # print("warm_start " + str(qpalm._settings.contents.warm_start))
    # print("reset_newton_iter " + str(qpalm._settings.contents.reset_newton_iter))
    # print("enable_dual_termination " + str(qpalm._settings.contents.enable_dual_termination))
    # print("time_limit " + str(qpalm._settings.contents.time_limit))
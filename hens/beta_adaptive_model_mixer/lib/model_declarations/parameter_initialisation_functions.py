# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from .bound_generators import *

def u_init(model, i, j):
    return (1/model.Hh[i]) + (1/model.Hc[j])

def u_cu_init(model, i):
    return (1/model.Hh[i]) + (1/model.H_cu)

def u_hu_init(model, j):
    return (1/model.Hc[j]) + (1/model.H_hu)

def u_beta_init(model, i, j):
    return pow(model.U[i,j], model.Beta)

def u_cu_beta_init(model, i):
    return pow(model.U_cu[i], model.Beta)

def u_hu_beta_init(model, j):
    return pow(model.U_hu[j], model.Beta)

def ech_init(model, i):
    return model.Fh[i]*(model.Th_in[i] - model.Th_out[i])

def ecc_init(model, j):
    return model.Fc[j]*(model.Tc_out[j] - model.Tc_in[j])

def omega_ij_init(model, i, j):
    return min(model.Ech[i], model.Ecc[j])

def omega_i_init(model, i):
    return model.Ech[i]

def omega_j_init(model, j):
    return model.Ecc[j]

def gamma_init(model, i, j):
    return  max(\
                0,\
                model.Tc_in[j] - model.Th_in[i],\
                model.Tc_in[j] - model.Th_out[i],\
                model.Tc_out[j] - model.Th_in[i],\
                model.Tc_out[j] - model.Th_out[i]\
            )

def th_breakpoints_init(model, i):
    return list(th_bounds(model, i))

def thx_breakpoints_init(model, i, j, k):
    return list(thx_bounds(model, i, j, k))

def tc_breakpoints_init(model, j):
    return list(tc_bounds(model, j))

def tcx_breakpoints_init(model, i, j, k):
    return list(tcx_bounds(model, i, j, k))

def q_beta_breakpoints_init(model, i, j, *k):
    return list(q_bounds(model, i, j))

def q_cu_beta_breakpoints_init(model, i):
    return list(q_cu_bounds(model, i))

def q_hu_beta_breakpoints_init(model, j):
    return list(q_hu_bounds(model, j))

def q_beta_gradients_init(model, i, j, k):
    gradients = [0]*(len(model.Q_beta_breakpoints[i,j,k])-1)
    for m in range(1, len(model.Q_beta_breakpoints[i,j,k])):
        numerator = model.Q_beta_exp[i,j,k][m+1] - model.Q_beta_exp[i,j,k][m]
        denominator = model.Q_beta_breakpoints[i,j,k][m+1] - model.Q_beta_breakpoints[i,j,k][m]
        gradients[m-1] = numerator/denominator
    return gradients

def q_cu_beta_gradients_init(model, i):
    gradients = [0]*(len(model.Q_cu_beta_breakpoints[i])-1)
    for m in range(1, len(model.Q_cu_beta_breakpoints[i])):
        numerator = model.Q_cu_beta_exp[i][m+1] - model.Q_cu_beta_exp[i][m]
        denominator = model.Q_cu_beta_breakpoints[i][m+1] - model.Q_cu_beta_breakpoints[i][m]
        gradients[m-1] = numerator/denominator
    return gradients

def q_hu_beta_gradients_init(model, j):
    gradients = [0]*(len(model.Q_hu_beta_breakpoints[j])-1)
    for m in range(1, len(model.Q_hu_beta_breakpoints[j])):
        numerator = model.Q_hu_beta_exp[j][m+1] - model.Q_hu_beta_exp[j][m]
        denominator = model.Q_hu_beta_breakpoints[j][m+1] - model.Q_hu_beta_breakpoints[j][m]
        gradients[m-1] = numerator/denominator
    return gradients

def area_beta_q_breakpoints_init(model, i, j, *k):
    return list(q_beta_bounds(model, i, j))

def area_beta_q_cu_breakpoints_init(model, i):
    return list(q_cu_beta_bounds(model, i))

def area_beta_q_hu_breakpoints_init(model, j):
    return list(q_hu_beta_bounds(model, j))

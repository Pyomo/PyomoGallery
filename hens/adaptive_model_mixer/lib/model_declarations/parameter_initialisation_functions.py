# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from .bound_generators import area_bounds, area_cu_bounds, area_hu_bounds, q_bounds, q_cu_bounds, q_hu_bounds, th_bounds, thx_bounds, tc_bounds, tcx_bounds

def u_init(model, i, j):
    return (1/model.Hh[i]) + (1/model.Hc[j])

def u_cu_init(model, i):
    return (1/model.Hh[i]) + (1/model.H_cu)

def u_hu_init(model, j):
    return (1/model.Hc[j]) + (1/model.H_hu)

def ech_init(model, i):
    return model.Fh[i]*(model.Th_in[i] - model.Th_out[i])

def ecc_init(model, j):
    return model.Fc[j]*(model.Tc_out[j] - model.Tc_in[j])

def Omega_ij_init(model, i, j):
    return min(model.Ech[i], model.Ecc[j])

def Omega_i_init(model, i):
    return model.Ech[i]

def Omega_j_init(model, j):
    return model.Ecc[j]

def Gamma_init(model, i, j):
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

def q_breakpoints_init(model, i, j, *k):
    return list(q_bounds(model, i, j))

def q_cu_breakpoints_init(model, i):
    return list(q_cu_bounds(model, i))

def q_hu_breakpoints_init(model, j):
    return list(q_hu_bounds(model, j))

def area_beta_breakpoints_init(model, i, j, *k):
    return list(area_bounds(model, i, j))

def area_beta_gradients_init(model, i, j, k):
    gradients = [0]*(len(model.Area_beta_breakpoints[i,j,k])-1)
    for m in range(1,len(model.Area_beta_breakpoints[i,j,k])):
        numerator = model.Area_beta_exp[i,j,k][m+1] - model.Area_beta_exp[i,j,k][m]
        denominator = model.Area_beta_breakpoints[i,j,k][m+1] - model.Area_beta_breakpoints[i,j,k][m]
        gradients[m-1] = numerator/denominator
    return gradients

def area_cu_beta_breakpoints_init(model, i):
    return list(area_cu_bounds(model, i))

def area_cu_beta_gradients_init(model, i):
    gradients = [0]*(len(model.Area_cu_beta_breakpoints[i])-1)
    for m in range(1,len(model.Area_cu_beta_breakpoints[i])):
        numerator = model.Area_cu_beta_exp[i][m+1] - model.Area_cu_beta_exp[i][m]
        denominator = model.Area_cu_beta_breakpoints[i][m+1] - model.Area_cu_beta_breakpoints[i][m]
        gradients[m-1] = numerator/denominator
    return gradients

def area_hu_beta_breakpoints_init(model, j):
    return list(area_hu_bounds(model, j))

def area_hu_beta_gradients_init(model, j):
    gradients = [0]*(len(model.Area_hu_beta_breakpoints[j])-1)
    for m in range(1,len(model.Area_hu_beta_breakpoints[j])):
        numerator = model.Area_hu_beta_exp[j][m+1] - model.Area_hu_beta_exp[j][m]
        denominator = model.Area_hu_beta_breakpoints[j][m+1] - model.Area_hu_beta_breakpoints[j][m]
        gradients[m-1] = numerator/denominator
    return gradients

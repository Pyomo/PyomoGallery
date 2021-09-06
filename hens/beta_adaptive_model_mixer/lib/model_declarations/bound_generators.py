# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from .helper_functions import lmtd_inv_beta

def fh_bounds(model, i, j, k):
    return (0, model.Fh[i])

def fc_bounds(model, i, j, k):
    return (0, model.Fc[j])

def thx_bounds(model, i, j, k):
    return (model.Th_out[i], model.Th_in[i])

def tcx_bounds(model, i, j, k):
    return (model.Tc_in[j], model.Tc_out[j])

def dt_bounds(model, i, j, k):
    return (model.Delta_t_min, model.Th_in[i]-model.Tc_in[j])

def dt_cu_bounds(model, i):
    return (model.Delta_t_min, model.Th_in[i]-model.T_cu_in)

def dt_hu_bounds(model, j):
    return (model.Delta_t_min, model.T_hu_in - model.Tc_in[j])

def reclmtd_beta_bounds(model, i, j, *k):
    xy_min = model.Delta_t_min
    xy_max = model.Th_in[i] - model.Tc_in[j]

    reclmtd_beta_lower = lmtd_inv_beta(xy_max, xy_max, model.Beta)
    reclmtd_beta_upper = lmtd_inv_beta(xy_min, xy_min, model.Beta)

    return (reclmtd_beta_lower, reclmtd_beta_upper)

def reclmtd_cu_beta_bounds(model, i):
    x_min = model.Delta_t_min
    x_max = model.Th_in[i] - model.T_cu_out
    y    = model.Th_out[i] - model.T_cu_in

    reclmtd_beta_cu_lower = lmtd_inv_beta(x_max, y, model.Beta)
    reclmtd_beta_cu_upper = lmtd_inv_beta(x_min, y, model.Beta)

    return (reclmtd_beta_cu_lower, reclmtd_beta_cu_upper)

def reclmtd_hu_beta_bounds(model, j):
    x_min = model.Delta_t_min
    x_max = model.T_hu_out - model.Tc_in[j]
    y    = model.T_hu_in - model.Tc_out[j]

    reclmtd_beta_hu_lower = lmtd_inv_beta(x_max, y, model.Beta)
    reclmtd_beta_hu_upper = lmtd_inv_beta(x_min, y, model.Beta)

    return (reclmtd_beta_hu_lower, reclmtd_beta_hu_upper)

def q_bounds(model, i, j, *k):
    q_lower = 0

    q_upper_hot_side  = model.Fh[i]*(model.Th_in[i] - model.Th_out[i])
    q_upper_cold_side = model.Fc[j]*(model.Tc_out[j] - model.Tc_in[j])
    q_upper = min( q_upper_hot_side, q_upper_cold_side )
    return (q_lower, q_upper)

def q_cu_bounds(model, i):
    q_cu_lower = 0
    q_cu_upper = model.Fh[i]*(model.Th_in[i] - model.Th_out[i])
    return (q_cu_lower, q_cu_upper)

def q_hu_bounds(model, j):
    q_hu_lower = 0
    q_hu_upper = model.Fc[j]*(model.Tc_out[j] - model.Tc_in[j])
    return (q_hu_lower, q_hu_upper)

def q_beta_bounds(model, i, j, *k):
    q_bounds_val = q_bounds(model, i, j)
    return q_bounds_val if (model.Beta == 1) else tuple(map(lambda q: pow(q, model.Beta), q_bounds_val))

def q_cu_beta_bounds(model, i):
    q_cu_bounds_val = q_cu_bounds(model, i)
    return q_cu_bounds_val if (model.Beta == 1) else tuple(map(lambda q: pow(q, model.Beta), q_cu_bounds_val))

def q_hu_beta_bounds(model, j):
    q_hu_bounds_val = q_hu_bounds(model, j)
    return q_hu_bounds_val if (model.Beta == 1) else tuple(map(lambda q: pow(q, model.Beta), q_hu_bounds_val))

def th_bounds(model, i, *k):
    return (model.Th_out[i], model.Th_in[i])

def tc_bounds(model, j, *k):
    return (model.Tc_in[j], model.Tc_out[j])

def bh_bounds(model, i, j, k):
    return (0, model.Th_in[i]*model.Fh[i])

def bc_bounds(model, i, j, k):
    return (0, model.Tc_out[j]*model.Fc[j])

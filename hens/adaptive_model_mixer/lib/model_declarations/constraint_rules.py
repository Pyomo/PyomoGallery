# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from .helper_functions import lmtd_inverse_gradient_calculator, lmtd_inv

from pyomo.core.base.constraint import Constraint

def z_th_sum_rule(model, i, k):
    return sum(model.z_th[i,k,n] for n in range(1, len(model.Th_breakpoints[i,k])) ) == 1

def th_lower_rule(model, i, k):
    return model.th[i,k] >= sum(model.Th_breakpoints[i,k][n]*model.z_th[i,k,n] for n in range(1, len(model.Th_breakpoints[i,k])))

def th_upper_rule(model, i, k):
    return model.th[i,k] <= sum(model.Th_breakpoints[i,k][n+1]*model.z_th[i,k,n] for n in range(1, len(model.Th_breakpoints[i,k])))

def var_delta_fh_sum_rule(model, i, j, k):
    return model.fh[i,j,k] == sum(model.var_delta_fh[i,j,k,n] for n in range(1, len(model.Th_breakpoints[i,k])))

def var_delta_fh_upper_rule(model, i, j, k, n):
    return model.var_delta_fh[i,j,k,n] <= model.Fh[i]*model.z_th[i,k,n]

##########################
def z_thx_sum_rule(model, i, j, k):
    return sum(model.z_thx[i,j,k,n] for n in range(1, len(model.Thx_breakpoints[i,j,k])) ) == 1

def thx_lower_rule(model, i, j, k):
    return model.thx[i,j,k] >= sum(model.Thx_breakpoints[i,j,k][n]*model.z_thx[i,j,k,n] for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def thx_upper_rule(model, i, j, k):
    return model.thx[i,j,k] <= sum(model.Thx_breakpoints[i,j,k][n+1]*model.z_thx[i,j,k,n] for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def var_delta_fhx_sum_rule(model, i, j, k):
    return model.fh[i,j,k] == sum(model.var_delta_fhx[i,j,k,n] for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def var_delta_fhx_upper_rule(model, i, j, k, n):
    return model.var_delta_fhx[i,j,k,n] <= model.Fh[i]*model.z_thx[i,j,k,n]

##########################
def z_tc_sum_rule(model, j, k):
    return sum(model.z_tc[j,k+1,n] for n in range(1, len(model.Tc_breakpoints[j,k+1])) ) == 1

def tc_lower_rule(model, j, k):
    return model.tc[j,k+1] >= sum(model.Tc_breakpoints[j,k+1][n]*model.z_tc[j,k+1,n] for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def tc_upper_rule(model, j, k):
    return model.tc[j,k+1] <= sum(model.Tc_breakpoints[j,k+1][n+1]*model.z_tc[j,k+1,n] for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def var_delta_fc_sum_rule(model, i, j, k):
    return model.fc[i,j,k] == sum(model.var_delta_fc[i,j,k,n] for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def var_delta_fc_upper_rule(model, i, j, k, n):
    return model.var_delta_fc[i,j,k,n] <= model.Fc[j]*model.z_tc[j,k+1,n]

##########################
def z_tcx_sum_rule(model, i, j, k):
    return sum(model.z_tcx[i,j,k,n] for n in range(1, len(model.Tcx_breakpoints[i,j,k])) ) == 1

def tcx_lower_rule(model, i, j, k):
    return model.tcx[i,j,k] >= sum(model.Tcx_breakpoints[i,j,k][n]*model.z_tcx[i,j,k,n] for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def tcx_upper_rule(model, i, j, k):
    return model.tcx[i,j,k] <= sum(model.Tcx_breakpoints[i,j,k][n+1]*model.z_tcx[i,j,k,n] for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def var_delta_fcx_sum_rule(model, i, j, k):
    return model.fc[i,j,k] == sum(model.var_delta_fcx[i,j,k,n] for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def var_delta_fcx_upper_rule(model, i, j, k, n):
    return model.var_delta_fcx[i,j,k,n] <= model.Fc[j]*model.z_tcx[i,j,k,n]

##########################

##########################
def z_q_sum_rule(model, i, j, k):
    return sum(model.z_q[i,j,k,n] for n in range(1, len(model.Q_breakpoints[i,j,k])) ) == 1

def q_lower_rule(model, i, j, k):
    return model.q[i,j,k] >= sum(model.Q_breakpoints[i,j,k][n]*model.z_q[i,j,k,n] for n in range(1, len(model.Q_breakpoints[i,j,k])))

def q_upper_rule(model, i, j, k):
    return model.q[i,j,k] <= sum(model.Q_breakpoints[i,j,k][n+1]*model.z_q[i,j,k,n] for n in range(1, len(model.Q_breakpoints[i,j,k])))

def var_delta_reclmtd_sum_rule(model, i, j, k):
    reclmtd_lower, _ = model.reclmtd[i,j,k].bounds
    return model.reclmtd[i,j,k] == reclmtd_lower + sum(model.var_delta_reclmtd[i,j,k,n] for n in range(1, len(model.Q_breakpoints[i,j,k])))

def var_delta_reclmtd_upper_rule(model, i, j, k, n):
    reclmtd_lower, reclmtd_upper = model.reclmtd[i,j,k].bounds
    return model.var_delta_reclmtd[i,j,k,n] <= (reclmtd_upper-reclmtd_lower)*model.z_q[i,j,k,n]

##########################
def z_q_cu_sum_rule(model, i):
    return sum(model.z_q_cu[i,n] for n in range(1, len(model.Q_cu_breakpoints[i])) ) == 1

def q_cu_lower_rule(model, i):
    return model.q_cu[i] >= sum(model.Q_cu_breakpoints[i][n]*model.z_q_cu[i,n] for n in range(1, len(model.Q_cu_breakpoints[i])))

def q_cu_upper_rule(model, i):
    return model.q_cu[i] <= sum(model.Q_cu_breakpoints[i][n+1]*model.z_q_cu[i,n] for n in range(1, len(model.Q_cu_breakpoints[i])))

def var_delta_reclmtd_cu_sum_rule(model, i):
    reclmtd_cu_lower, _ = model.reclmtd_cu[i].bounds
    return model.reclmtd_cu[i] == reclmtd_cu_lower + sum(model.var_delta_reclmtd_cu[i,n] for n in range(1, len(model.Q_cu_breakpoints[i])))

def var_delta_reclmtd_cu_upper_rule(model, i, n):
    reclmtd_cu_lower, reclmtd_cu_upper = model.reclmtd_cu[i].bounds
    return model.var_delta_reclmtd_cu[i,n] <= (reclmtd_cu_upper-reclmtd_cu_lower)*model.z_q_cu[i,n]

##########################
def z_q_hu_sum_rule(model, j):
    return sum(model.z_q_hu[j,n] for n in range(1, len(model.Q_hu_breakpoints[j])) ) == 1

def q_hu_lower_rule(model, j):
    return model.q_hu[j] >= sum(model.Q_hu_breakpoints[j][n]*model.z_q_hu[j,n] for n in range(1, len(model.Q_hu_breakpoints[j])))

def q_hu_upper_rule(model, j):
    return model.q_hu[j] <= sum(model.Q_hu_breakpoints[j][n+1]*model.z_q_hu[j,n] for n in range(1, len(model.Q_hu_breakpoints[j])))

def var_delta_reclmtd_hu_sum_rule(model, j):
    reclmtd_hu_lower, _ = model.reclmtd_hu[j].bounds
    return model.reclmtd_hu[j] == reclmtd_hu_lower + sum(model.var_delta_reclmtd_hu[j,n] for n in range(1, len(model.Q_hu_breakpoints[j])))

def var_delta_reclmtd_hu_upper_rule(model, j, n):
    reclmtd_hu_lower, reclmtd_hu_upper = model.reclmtd_hu[j].bounds
    return model.var_delta_reclmtd_hu[j,n] <= (reclmtd_hu_upper-reclmtd_hu_lower)*model.z_q_hu[j,n]

##########################
def overall_heat_balance_hot_rule(model, i):
    return ( sum(model.q[i,j,k] for j in model.CP for k in model.ST ) + model.q_cu[i] ) == model.Fh[i]*(model.Th_in[i] - model.Th_out[i])

def overall_heat_balance_cold_rule(model, j):
    return ( sum(model.q[i,j,k] for i in model.HP for k in model.ST ) + model.q_hu[j] ) == model.Fc[j]*(model.Tc_out[j] - model.Tc_in[j])

def energy_balance_hot_rule(model, i, k):
    return sum( model.q[i,j,k] for j in model.CP ) == model.Fh[i]*(model.th[i,k] - model.th[i,k+1])

def energy_balance_cold_rule(model, j, k):
    return sum( model.q[i,j,k] for i in model.HP ) == model.Fc[j]*(model.tc[j,k] - model.tc[j, k+1])

def energy_balance_cu_rule(model, i):
    return model.Fh[i]*( model.th[i,model.Number_stages+1] - model.Th_out[i] ) == model.q_cu[i]

def energy_balance_hu_rule(model, j):
    return model.Fc[j]*( model.Tc_out[j] - model.tc[j,1] ) == model.q_hu[j]

def hot_inlet_rule(model, i):
    return model.th[i, 1] == model.Th_in[i]

def cold_inlet_rule(model, j):
    return model.tc[j,model.Number_stages+1] == model.Tc_in[j]

def mass_balance_hot_rule(model, i, k):
    return sum( model.fh[i,j,k] for j in model.CP ) == model.Fh[i]

def mass_balance_cold_rule(model, j, k):
    return sum( model.fc[i,j,k] for i in model.HP ) == model.Fc[j]

def decreasing_hot_rule(model, i, k):
    return model.th[i,k+1] <= model.th[i,k]

def decreasing_cold_rule(model, j, k):
    return model.tc[j,k+1] <= model.tc[j,k]

def hot_upper_bound_rule(model, i):
    return model.th[i, model.Number_stages+1] >= model.Th_out[i]

def cold_lower_bound_rule(model, j):
    return model.tc[j,1] <= model.Tc_out[j]

def q_big_m_rule(model, i, j, k):
    return model.q[i,j,k] - model.Omega_ij[i,j]*model.z[i,j,k] <= 0

def q_cu_big_m_rule(model, i):
    return model.q_cu[i] - model.Omega_i[i]*model.z_cu[i] <= 0

def q_hu_big_m_rule(model, j):
    return model.q_hu[j] - model.Omega_j[j]*model.z_hu[j] <= 0

def temp_app_in_rule(model, i, j, k):
    return model.dt[i,j,k] <= model.th[i,k] - model.tc[j,k] + model.Gamma[i,j]*(1 - model.z[i,j,k])

def temp_app_out_rule(model, i, j, k):
    return model.dt[i,j,k+1] <= model.th[i,k+1] - model.tc[j,k+1] + model.Gamma[i,j]*(1 - model.z[i,j,k])

def temp_app_cu_rule(model, i):
    return model.dt_cu[i] <= model.th[i,model.Number_stages + 1] - model.T_cu_out

def temp_app_hu_rule(model, j):
    return model.dt_hu[j] <= model.T_hu_out - model.tc[j,1]

def mccor_convex_h_in_1_rule(model, i, j, k):
    return  model.bh_in[i,j,k] >=\
            sum(model.Th_breakpoints[i,k][n]*model.var_delta_fh[i,j,k,n] \
                for n in range(1, len(model.Th_breakpoints[i,k])))

def mccor_convex_h_in_2_rule(model, i, j, k):
    return  model.bh_in[i,j,k] >=\
            model.th[i,k]*model.Fh[i] +\
            sum(model.Th_breakpoints[i,k][n+1]*\
                (model.var_delta_fh[i,j,k,n] - model.Fh[i]*model.z_th[i,k,n]) \
                for n in range(1, len(model.Th_breakpoints[i,k])))

def mccor_concave_h_in_1_rule(model, i, j, k):
    return  model.bh_in[i,j,k] <=\
            sum(model.Th_breakpoints[i,k][n+1]*model.var_delta_fh[i,j,k,n] \
                for n in range(1, len(model.Th_breakpoints[i,k])))

def mccor_concave_h_in_2_rule(model, i, j, k):
    return  model.bh_in[i,j,k] <=\
            model.th[i,k]*model.Fh[i] +\
            sum(model.Th_breakpoints[i,k][n]*\
                (model.var_delta_fh[i,j,k,n] - model.Fh[i]*model.z_th[i,k,n]) \
                for n in range(1, len(model.Th_breakpoints[i,k])))

def mccor_convex_h_out_1_rule(model, i, j, k):
    return  model.bh_out[i,j,k] >= \
            sum(model.Thx_breakpoints[i,j,k][n]*model.var_delta_fhx[i,j,k,n] \
                for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def mccor_convex_h_out_2_rule(model, i, j, k):
    return  model.bh_out[i,j,k] >= \
            model.thx[i,j,k]*model.Fh[i] +\
            sum(model.Thx_breakpoints[i,j,k][n+1]*\
                (model.var_delta_fhx[i,j,k,n] - model.Fh[i]*model.z_thx[i,j,k,n]) \
                for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def mccor_concave_h_out_1_rule(model, i, j, k):
    return  model.bh_out[i,j,k] <= \
            sum(model.Thx_breakpoints[i,j,k][n+1]*model.var_delta_fhx[i,j,k,n] \
                for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def mccor_concave_h_out_2_rule(model, i, j, k):
    return  model.bh_out[i,j,k] <= \
            model.thx[i,j,k]*model.Fh[i] +\
            sum(model.Thx_breakpoints[i,j,k][n]*\
                (model.var_delta_fhx[i,j,k,n] - model.Fh[i]*model.z_thx[i,j,k,n]) \
                for n in range(1, len(model.Thx_breakpoints[i,j,k])))

def mccor_convex_c_in_1_rule(model, i, j, k):
    return  model.bc_in[i,j,k] >=\
            sum(model.Tc_breakpoints[j,k+1][n]*model.var_delta_fc[i,j,k,n] \
                for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def mccor_convex_c_in_2_rule(model, i, j, k):
    return  model.bc_in[i,j,k] >= \
            model.tc[j,k+1]*model.Fc[j] + \
            sum(model.Tc_breakpoints[j,k+1][n+1]*\
                (model.var_delta_fc[i,j,k,n] - model.Fc[j]*model.z_tc[j,k+1,n]) \
                for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def mccor_concave_c_in_1_rule(model, i, j, k):
    return  model.bc_in[i,j,k] <= \
            sum(model.Tc_breakpoints[j,k+1][n+1]*model.var_delta_fc[i,j,k,n] \
                for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def mccor_concave_c_in_2_rule(model, i, j, k):
    return  model.bc_in[i,j,k] <= \
            model.tc[j,k+1]*model.Fc[j] + \
            sum(model.Tc_breakpoints[j,k+1][n]*\
                (model.var_delta_fc[i,j,k,n] - model.Fc[j]*model.z_tc[j,k+1,n]) \
                for n in range(1, len(model.Tc_breakpoints[j,k+1])))

def mccor_convex_c_out_1_rule(model, i, j, k):
    return  model.bc_out[i,j,k] >= \
            sum(model.Tcx_breakpoints[i,j,k][n]*model.var_delta_fcx[i,j,k,n] \
                for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def mccor_convex_c_out_2_rule(model, i, j, k):
    return  model.bc_out[i,j,k] >= \
            model.tcx[i,j,k]*model.Fc[j] + \
            sum(model.Tcx_breakpoints[i,j,k][n+1]*\
                (model.var_delta_fcx[i,j,k,n] - model.Fc[j]*model.z_tcx[i,j,k,n]) \
                for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def mccor_concave_c_out_1_rule(model, i, j, k):
    return  model.bc_out[i,j,k] <= \
            sum(model.Tcx_breakpoints[i,j,k][n+1]*model.var_delta_fcx[i,j,k,n] \
                for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def mccor_concave_c_out_2_rule(model, i, j, k):
    return  model.bc_out[i,j,k] <= \
            model.tcx[i,j,k]*model.Fc[j] + \
            sum(model.Tcx_breakpoints[i,j,k][n]*\
                (model.var_delta_fcx[i,j,k,n] - model.Fc[j]*model.z_tcx[i,j,k,n])\
                for n in range(1, len(model.Tcx_breakpoints[i,j,k])))

def mixer_energy_bal_hot_rule(model, i, k):
    return model.Fh[i]*model.th[i,k+1] == sum( model.bh_out[i,j,k] for j in model.CP)

def mixer_energy_bal_cold_rule(model, j, k):
    return model.Fc[j]*model.tc[j,k]   == sum( model.bc_out[i,j,k] for i in model.HP)

def q_energy_bal_hot_rule(model, i, j, k):
    return model.q[i,j,k] == (model.bh_in[i,j,k] - model.bh_out[i,j,k])

def q_energy_bal_cold_rule(model, i, j, k):
    return model.q[i,j,k] == (model.bc_out[i,j,k] - model.bc_in[i,j,k])

# A_ijk
def area_mccor_convex_1_rule(model, i, j, k):
    reclmtd_lower, _ = model.reclmtd[i,j,k].bounds
    return  model.area[i,j,k] >= \
            model.U[i,j]*(\
                model.q[i,j,k]*reclmtd_lower +\
                sum( \
                    model.Q_breakpoints[i,j,k][n]*model.var_delta_reclmtd[i,j,k,n] \
                    for n in range(1, len(model.Q_breakpoints[i,j,k]))) \
            )

def area_mccor_convex_2_rule(model, i, j, k):
    reclmtd_lower, reclmtd_upper = model.reclmtd[i,j,k].bounds
    return  model.area[i,j,k] >= \
            model.U[i,j]*(\
                model.q[i,j,k]*reclmtd_upper + \
                sum( \
                    model.Q_breakpoints[i,j,k][n+1]* \
                    (model.var_delta_reclmtd[i,j,k,n] - (reclmtd_upper-reclmtd_lower)*model.z_q[i,j,k,n])\
                    for n in range(1, len(model.Q_breakpoints[i,j,k]))) \
            )

def area_mccor_concave_1_rule(model, i, j, k):
    reclmtd_lower, _ = model.reclmtd[i,j,k].bounds
    return  model.area[i,j,k] <= \
            model.U[i,j]*( \
                model.q[i,j,k]*reclmtd_lower + \
                sum( \
                    model.Q_breakpoints[i,j,k][n+1]*model.var_delta_reclmtd[i,j,k,n]\
                    for n in range(1, len(model.Q_breakpoints[i,j,k])))\
            )

def area_mccor_concave_2_rule(model, i, j, k):
    reclmtd_lower, reclmtd_upper = model.reclmtd[i,j,k].bounds
    return  model.area[i,j,k] <= \
            model.U[i,j]*(\
                model.q[i,j,k]*reclmtd_upper + \
                sum( \
                    model.Q_breakpoints[i,j,k][n]* \
                    (model.var_delta_reclmtd[i,j,k,n] - (reclmtd_upper-reclmtd_lower)*model.z_q[i,j,k,n])\
                    for n in range(1, len(model.Q_breakpoints[i,j,k]))) \
            )

# A_cui
def area_cu_mccor_convex_1_rule(model, i):
    reclmtd_cu_lower, _ = model.reclmtd_cu[i].bounds
    return  model.area_cu[i] >= \
            model.U_cu[i]*(\
                model.q_cu[i]*reclmtd_cu_lower +\
                sum(\
                    model.Q_cu_breakpoints[i][n]*model.var_delta_reclmtd_cu[i,n]\
                    for n in range(1, len(model.Q_cu_breakpoints[i])))\
            )

def area_cu_mccor_convex_2_rule(model, i):
    reclmtd_cu_lower, reclmtd_cu_upper = model.reclmtd_cu[i].bounds
    return  model.area_cu[i] >= \
            model.U_cu[i]*(\
                model.q_cu[i]*reclmtd_cu_upper +\
                sum(\
                    model.Q_cu_breakpoints[i][n+1]*\
                    (model.var_delta_reclmtd_cu[i,n] - (reclmtd_cu_upper - reclmtd_cu_lower)*model.z_q_cu[i,n])\
                    for n in range(1, len(model.Q_cu_breakpoints[i])))\
            )

def area_cu_mccor_concave_1_rule(model, i):
    reclmtd_cu_lower, _ = model.reclmtd_cu[i].bounds
    return  model.area_cu[i] <= \
            model.U_cu[i]*(\
                model.q_cu[i]*reclmtd_cu_lower +\
                sum(\
                    model.Q_cu_breakpoints[i][n+1]*model.var_delta_reclmtd_cu[i,n]\
                    for n in range(1, len(model.Q_cu_breakpoints[i])))\
            )

def area_cu_mccor_concave_2_rule(model, i):
    reclmtd_cu_lower, reclmtd_cu_upper = model.reclmtd_cu[i].bounds
    return  model.area_cu[i] <= \
            model.U_cu[i]*(\
                model.q_cu[i]*reclmtd_cu_upper +\
                sum(\
                    model.Q_cu_breakpoints[i][n]*\
                    (model.var_delta_reclmtd_cu[i,n] - (reclmtd_cu_upper - reclmtd_cu_lower)*model.z_q_cu[i,n])\
                    for n in range(1, len(model.Q_cu_breakpoints[i])))\
            )

# A_huj
def area_hu_mccor_convex_1_rule(model, j):
    reclmtd_hu_lower, _ = model.reclmtd_hu[j].bounds
    return  model.area_hu[j] >= \
            model.U_hu[j]*(\
                model.q_hu[j]*reclmtd_hu_lower +\
                sum(\
                    model.Q_hu_breakpoints[j][n]*model.var_delta_reclmtd_hu[j,n]\
                    for n in range(1, len(model.Q_hu_breakpoints[j])))\
            )

def area_hu_mccor_convex_2_rule(model, j):
    reclmtd_hu_lower, reclmtd_hu_upper = model.reclmtd_hu[j].bounds
    return  model.area_hu[j] >= \
            model.U_hu[j]*(\
                model.q_hu[j]*reclmtd_hu_upper +\
                sum(\
                    model.Q_hu_breakpoints[j][n+1]*\
                    (model.var_delta_reclmtd_hu[j,n] - (reclmtd_hu_upper - reclmtd_hu_lower)*model.z_q_hu[j,n])\
                    for n in range(1, len(model.Q_hu_breakpoints[j])))\
            )

def area_hu_mccor_concave_1_rule(model, j):
    reclmtd_hu_lower, _ = model.reclmtd_hu[j].bounds
    return  model.area_hu[j] <= \
            model.U_hu[j]*(\
                model.q_hu[j]*reclmtd_hu_lower +\
                sum(\
                    model.Q_hu_breakpoints[j][n+1]*model.var_delta_reclmtd_hu[j,n]\
                    for n in range(1, len(model.Q_hu_breakpoints[j])))\
            )

def area_hu_mccor_concave_2_rule(model, j):
    reclmtd_hu_lower, reclmtd_hu_upper = model.reclmtd_hu[j].bounds
    return  model.area_hu[j] <= \
            model.U_hu[j]*(\
                model.q_hu[j]*reclmtd_hu_upper +\
                sum(\
                    model.Q_hu_breakpoints[j][n]*\
                    (model.var_delta_reclmtd_hu[j,n] - (reclmtd_hu_upper - reclmtd_hu_lower)*model.z_q_hu[j,n])\
                    for n in range(1, len(model.Q_hu_breakpoints[j])))\
            )

# LMTD
def grad_reclmtd_rule(model, i, j, k, x0, y0):
    if x0 <= 0 or y0 <= 0:
        return Constraint.Feasible
    gradients = lmtd_inverse_gradient_calculator(x0, y0)
    return model.reclmtd[i,j,k] >= lmtd_inv(x0, y0) + gradients[0]*(model.dt[i,j,k] - x0) + gradients[1]*(model.dt[i,j,k+1] - y0)

def grad_reclmtd_cu_rule(model, i, x0):
    y0 = model.Th_out[i] - model.T_cu_in
    gradients = lmtd_inverse_gradient_calculator(x0, y0)
    return model.reclmtd_cu[i] >= lmtd_inv(x0, y0) + gradients[0]*(model.dt_cu[i] - x0)

def grad_reclmtd_hu_rule(model, j, x0):
    y0 = model.T_hu_in - model.Tc_out[j]
    gradients = lmtd_inverse_gradient_calculator(x0, y0)
    return model.reclmtd_hu[j] >= lmtd_inv(x0, y0) + gradients[0]*(model.dt_hu[j] - x0)

def z_area_beta_sum_rule(model, i, j, k):
    return sum( model.z_area_beta[i,j,k,m] for m in range(1,len(model.Area_beta_breakpoints[i,j,k]))) == 1

def area_low_rule(model, i, j, k):
    if model.Beta == 1:
        return Constraint.Feasible
    else:
        area_lower = sum(model.z_area_beta[i,j,k,m]*model.Area_beta_breakpoints[i,j,k][m] for m in range(1,len(model.Area_beta_breakpoints[i,j,k])))
        return model.area[i,j,k] >= area_lower

def area_up_rule(model, i, j, k):
    if model.Beta == 1:
        return Constraint.Feasible
    else:
        area_upper = sum(model.z_area_beta[i,j,k,m]*model.Area_beta_breakpoints[i,j,k][m+1] for m in range(1,len(model.Area_beta_breakpoints[i,j,k])))
        return model.area[i,j,k] <= area_upper

def area_pow_beta_rule(model, i, j, k):
    if model.Beta == 1:
        return model.area_beta[i,j,k] == model.area[i,j,k]
    else:
        aread_lower = sum(model.z_area_beta[i,j,k,m]*model.Area_beta_breakpoints[i,j,k][m] for m in range(1,len(model.Area_beta_breakpoints[i,j,k])))
        aread_exp_lower = sum(model.z_area_beta[i,j,k,m]*model.Area_beta_exp[i,j,k][m] for m in range(1,len(model.Area_beta_breakpoints[i,j,k])))
        gradient = sum(model.z_area_beta[i,j,k,m]*model.Area_beta_gradients[i,j,k][m] for m in range(1,len(model.Area_beta_breakpoints[i,j,k])))
        return model.area_beta[i,j,k] >= aread_exp_lower + gradient*(model.area[i,j,k]- aread_lower)

def z_area_cu_beta_sum_rule(model, i):
    return sum( model.z_area_cu_beta[i,m] for m in range(1,len(model.Area_cu_beta_breakpoints[i]))) == 1

def area_cu_low_rule(model, i):
    if model.Beta == 1:
        return Constraint.Feasible
    else:
        area_cu_lower = sum(model.z_area_cu_beta[i,m]*model.Area_cu_beta_breakpoints[i][m] for m in range(1,len(model.Area_cu_beta_breakpoints[i])))
        return model.area_cu[i] >= area_cu_lower

def area_cu_up_rule(model, i):
    if model.Beta == 1:
        return Constraint.Feasible
    else:
        area_cu_upper = sum(model.z_area_cu_beta[i,m]*model.Area_cu_beta_breakpoints[i][m+1] for m in range(1,len(model.Area_cu_beta_breakpoints[i])))
        return model.area_cu[i] <= area_cu_upper

def area_cu_pow_beta_rule(model, i):
    if model.Beta == 1:
        return model.area_cu_beta[i] == model.area_cu[i]
    else:
        area_cu_lower = sum(model.z_area_cu_beta[i,m]*model.Area_cu_beta_breakpoints[i][m] for m in range(1,len(model.Area_cu_beta_breakpoints[i])))
        area_cu_exp_lower = sum(model.z_area_cu_beta[i,m]*model.Area_cu_beta_exp[i][m] for m in range(1,len(model.Area_cu_beta_breakpoints[i])))
        gradient = sum(model.z_area_cu_beta[i,m]*model.Area_cu_beta_gradients[i][m] for m in range(1,len(model.Area_cu_beta_breakpoints[i])))
        return model.area_cu_beta[i] >= area_cu_exp_lower + gradient*(model.area_cu[i]- area_cu_lower)

def z_area_hu_beta_sum_rule(model, j):
    return sum( model.z_area_hu_beta[j,m] for m in range(1,len(model.Area_hu_beta_breakpoints[j]))) == 1

def area_hu_low_rule(model, j):
    if model.Beta == 1:
        return Constraint.Feasible
    else:
        area_hu_lower = sum(model.z_area_hu_beta[j,m]*model.Area_hu_beta_breakpoints[j][m] for m in range(1,len(model.Area_hu_beta_breakpoints[j])))
        return model.area_hu[j] >= area_hu_lower

def area_hu_up_rule(model, j):
    if model.Beta == 1:
        return Constraint.Feasible
    else:
        area_hu_upper = sum(model.z_area_hu_beta[j,m]*model.Area_hu_beta_breakpoints[j][m+1] for m in range(1,len(model.Area_hu_beta_breakpoints[j])))
        return model.area_hu[j] <= area_hu_upper

def area_hu_pow_beta_rule(model, j):
    if model.Beta == 1:
        return model.area_hu_beta[j] == model.area_hu[j]
    else:
        area_hu_lower = sum(model.z_area_hu_beta[j,m]*model.Area_hu_beta_breakpoints[j][m] for m in range(1,len(model.Area_hu_beta_breakpoints[j])))
        area_hu_exp_lower = sum(model.z_area_hu_beta[j,m]*model.Area_hu_beta_exp[j][m] for m in range(1,len(model.Area_hu_beta_breakpoints[j])))
        gradient = sum(model.z_area_hu_beta[j,m]*model.Area_hu_beta_gradients[j][m] for m in range(1,len(model.Area_hu_beta_breakpoints[j])))
        return model.area_hu_beta[j] >= area_hu_exp_lower + gradient*(model.area_hu[j]- area_hu_lower)

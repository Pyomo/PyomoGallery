# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

import os

from pprint import pprint
from math import log

def check_eq1_feasibility(instance, feas_results):
    eq1_results = {}
    for i in instance.HP:
        local_result = {}
        rhs = instance.Fh[i]*(instance.Th_in[i] - instance.Th_out[i])
        lhs = instance.q_cu[i].value + sum(instance.q[i,j,k].value for j in instance.CP for k in instance.ST)
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq1_results[i] = local_result

    feas_results['eq01'] = eq1_results

def check_eq2_feasibility(instance, feas_results):
    eq2_results = {}
    for j in instance.CP:
        local_result = {}
        rhs = instance.Fc[j]*(instance.Tc_out[j] - instance.Tc_in[j])
        lhs = instance.q_hu[j].value + sum(instance.q[i,j,k].value for i in instance.HP for k in instance.ST)
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq2_results[j] = local_result

    feas_results['eq02'] = eq2_results

def check_eq3_feasibility(instance, feas_results):
    eq3_results = {}
    for i in instance.HP:
        for k in instance.ST:
            local_result = {}
            rhs = instance.Fh[i]
            lhs = sum(instance.fh[i,j,k].value for j in instance.CP)
            eps = rhs - lhs
            local_result['lhs'] = lhs
            local_result['rhs'] = rhs
            local_result['eps'] = eps
            eq3_results[(i,k)] = local_result

    feas_results['eq03'] = eq3_results

def check_eq4_feasibility(instance, feas_results):
    eq4_results = {}
    for j in instance.CP:
        for k in instance.ST:
            local_result = {}
            rhs = instance.Fc[j]
            lhs = sum(instance.fc[i,j,k].value for i in instance.HP)
            eps = rhs - lhs
            local_result['lhs'] = lhs
            local_result['rhs'] = rhs
            local_result['eps'] = eps
            eq4_results[(j,k)] = local_result

    feas_results['eq04'] = eq4_results

def check_eq5_feasibility(instance, feas_results):
    eq5_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                rhs = instance.fh[i,j,k].value*(instance.th[i,k].value - instance.thx[i,j,k].value)
                lhs = instance.q[i,j,k].value
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                local_result['eps'] = eps
                eq5_results[(i,j,k)] = local_result

    feas_results['eq05'] = eq5_results

def check_eq6_feasibility(instance, feas_results):
    eq6_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                rhs = instance.fc[i,j,k].value*(instance.tcx[i,j,k].value - instance.tc[j,k+1].value)
                lhs = instance.q[i,j,k].value
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                local_result['eps'] = eps
                eq6_results[(i,j,k)] = local_result

    feas_results['eq06'] = eq6_results

def check_eq7_feasibility(instance, feas_results):
    eq7_results = {}
    for i in instance.HP:
        for k in instance.ST:
            local_result = {}
            rhs = 0
            for j in instance.CP:
                rhs = sum(instance.fh[i,j,k].value *instance.thx[i,j,k].value for j in instance.CP)
            lhs = instance.Fh[i]*instance.th[i,k+1].value
            eps = rhs - lhs
            local_result['lhs'] = lhs
            local_result['rhs'] = rhs
            local_result['eps'] = eps
            eq7_results[(i,k)] = local_result

        feas_results['eq07'] = eq7_results

def check_eq8_feasibility(instance, feas_results):
    eq8_results = {}
    for j in instance.CP:
        for k in instance.ST:
            local_result = {}
            rhs = sum(instance.fc[i,j,k].value*instance.tcx[i,j,k].value for i in instance.HP)
            lhs = instance.Fc[j]*instance.tc[j,k].value
            eps = rhs - lhs
            local_result['lhs'] = lhs
            local_result['rhs'] = rhs
            local_result['eps'] = eps
            eq8_results[(j,k)] = local_result

    feas_results['eq08'] = eq8_results

def check_eq9_feasibility(instance, feas_results):
    eq9_results = {}
    for i in instance.HP:
        local_result = {}
        rhs = instance.Th_in[i]
        lhs = instance.th[i,1].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq9_results[i] = local_result

    feas_results['eq09'] = eq9_results

def check_eq10_feasibility(instance, feas_results):
    eq10_results = {}
    for j in instance.CP:
        local_result = {}
        rhs = instance.Tc_in[j]
        lhs = instance.tc[j,instance.Number_stages+1].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq10_results[j] = local_result

    feas_results['eq10'] = eq10_results

def check_eq11_feasibility(instance, feas_results):
    eq11_results = {}
    for i in instance.HP:
        local_result = {}
        rhs = instance.Fh[i]*(instance.th[i,instance.Number_stages+1].value-instance.Th_out[i])
        lhs = instance.q_cu[i].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq11_results[i] = local_result

    feas_results['eq11'] = eq11_results

def check_eq12_feasibility(instance, feas_results):
    eq12_results = {}
    for j in instance.CP:
        local_result = {}
        rhs = instance.Fc[j]*(instance.Tc_out[j]-instance.tc[j,1].value)
        lhs = instance.q_hu[j].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq12_results[j] = local_result

    feas_results['eq12'] = eq12_results

def check_eq13_feasibility(instance, feas_results):
    eq13_results = {}
    for i in instance.HP:
        for k in instance.ST:
            local_result = {}
            lhs = instance.th[i,k+1].value
            rhs = instance.th[i,k].value
            eps = rhs - lhs
            local_result['lhs'] = lhs
            local_result['rhs'] = rhs
            if lhs > rhs:
                local_result['eps'] = eps
            else:
                local_result['eps'] = 0
            eq13_results[(i,k)] = local_result

    feas_results['eq13'] = eq13_results

def check_eq14_feasibility(instance, feas_results):
    eq14_results = {}
    for j in instance.CP:
        for k in instance.ST:
            local_result = {}
            lhs = instance.tc[j,k+1].value
            rhs = instance.tc[j,k].value
            eps = rhs - lhs
            local_result['lhs'] = lhs
            local_result['rhs'] = rhs
            if lhs > rhs:
                local_result['eps'] = eps
            else:
                local_result['eps'] = 0
            eq14_results[(j,k)] = local_result

    feas_results['eq14'] = eq14_results

def check_eq15_feasibility(instance, feas_results):
    eq15_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.th[i,instance.Number_stages+1].value
        rhs = instance.Th_out[i]
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs < rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq15_results[i] = local_result

    feas_results['eq15'] = eq15_results

def check_eq16_feasibility(instance, feas_results):
    eq16_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.tc[j,1].value
        rhs = instance.Tc_out[j]
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs > rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq16_results[j] = local_result

    feas_results['eq16'] = eq16_results

def check_eq17_feasibility(instance, feas_results):
    eq17_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.q[i,j,k].value - instance.Omega_ij[i,j]*instance.z[i,j,k].value
                rhs = 0
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                if lhs > rhs:
                    local_result['eps'] = eps
                else:
                    local_result['eps'] = 0
                eq17_results[(i,j,k)] = local_result

    feas_results['eq17'] = eq17_results

def check_eq18_feasibility(instance, feas_results):
    eq18_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.q_cu[i].value - instance.Omega_i[i]*instance.z_cu[i].value
        rhs = 0
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs > rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq18_results[i] = local_result

    feas_results['eq18'] = eq18_results

def check_eq19_feasibility(instance, feas_results):
    eq19_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.q_hu[j].value - instance.Omega_j[j]*instance.z_hu[j].value
        rhs = 0
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs > rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq19_results[j] = local_result

    feas_results['eq19'] = eq19_results

def check_eq20_feasibility(instance, feas_results):
    eq20_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.dt[i,j,k].value
                rhs = instance.th[i,k].value - instance.tc[j,k].value + instance.Gamma[i,j]*(1-instance.z[i,j,k].value)
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                if lhs > rhs:
                    local_result['eps'] = eps
                else:
                    local_result['eps'] = 0
                eq20_results[(i,j,k)] = local_result

    feas_results['eq20'] = eq20_results

def check_eq21_feasibility(instance, feas_results):
    eq21_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.dt[i,j,k+1].value
                rhs = instance.th[i,k+1].value - instance.tc[j,k+1].value + instance.Gamma[i,j]*(1-instance.z[i,j,k].value)
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                if lhs > rhs:
                    local_result['eps'] = eps
                else:
                    local_result['eps'] = 0
                eq21_results[(i,j,k)] = local_result

    feas_results['eq21'] = eq21_results

def check_eq22_feasibility(instance, feas_results):
    eq22_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.dt_cu[i].value
        rhs = instance.th[i,instance.Number_stages+1].value - instance.T_cu_out
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs > rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq22_results[i] = local_result

    feas_results['eq22'] = eq22_results

def check_eq23_feasibility(instance, feas_results):
    eq23_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.dt_hu[j].value
        rhs = instance.T_hu_out - instance.tc[j,1].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs > rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq23_results[j] = local_result

    feas_results['eq23'] = eq23_results

def check_eq24_feasibility(instance, feas_results):
    eq24_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.dt[i,j,k].value
                rhs = instance.Delta_t_min.value
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                if lhs < rhs:
                    local_result['eps'] = eps
                else:
                    local_result['eps'] = 0
                eq24_results[(i,j,k)] = local_result

    feas_results['eq24'] = eq24_results

def check_eq25_feasibility(instance, feas_results):
    eq25_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.dt_cu[i].value
        rhs = instance.Delta_t_min.value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs < rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq25_results[i] = local_result

    feas_results['eq25'] = eq25_results

def check_eq26_feasibility(instance, feas_results):
    eq26_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.dt_hu[j].value
        rhs = instance.Delta_t_min.value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        if lhs < rhs:
            local_result['eps'] = eps
        else:
            local_result['eps'] = 0
        eq26_results[j] = local_result

    feas_results['eq26'] = eq26_results

#######################
# Note: _feasibility checks for 27, 29, 30 are for reclmtd^{beta}
######################
def check_eq27_feasibility(instance, feas_results):
    eq27_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.reclmtd_beta[i,j,k].value
                x = instance.dt[i,j,k].value
                y = instance.dt[i,j,k+1].value
                rhs = pow(1/x, instance.Beta) if x == y else pow(log(x/y)/(x-y), instance.Beta)
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                local_result['eps'] = eps
                eq27_results[(i,j,k)] = local_result

    feas_results['eq27'] = eq27_results

#######################
# Note: _feasibility checks for 28, 31, 32 are for A^{beta}
######################
def check_eq28_feasibility(instance, feas_results):
    eq28_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.area_beta[i,j,k].value
                u = pow(1/instance.Hh[i] + 1/instance.Hc[j], instance.Beta)
                rhs = instance.q_beta[i,j,k].value*u*instance.reclmtd_beta[i,j,k].value
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                local_result['eps'] = eps
                eq28_results[(i,j,k)] = local_result

    feas_results['eq28'] = eq28_results

#######################
# Note: _feasibility checks for 27, 29, 30 are for reclmtd^{beta}
######################
def check_eq29_feasibility(instance, feas_results):
    eq29_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.reclmtd_cu_beta[i].value
        x = instance.dt_cu[i].value
        y = instance.Th_out[i] - instance.T_cu_in
        rhs = pow(1/x, instance.Beta) if x == y else pow(log(x/y)/(x-y), instance.Beta)
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq29_results[i] = local_result

    feas_results['eq29'] = eq29_results

def check_eq30_feasibility(instance, feas_results):
    eq30_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.reclmtd_hu_beta[j].value
        x = instance.dt_hu[j].value
        y = instance.T_hu_in - instance.Tc_out[j]
        rhs = pow(1/x, instance.Beta) if x == y else pow(log(x/y)/(x-y), instance.Beta)
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq30_results[j] = local_result

    feas_results['eq30'] = eq30_results

#######################
# Note: _feasibility checks for 28, 31, 32 are for A^{beta}
######################
def check_eq31_feasibility(instance, feas_results):
    eq31_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.area_cu_beta[i].value
        u = pow(1/instance.Hh[i] + 1/instance.H_cu, instance.Beta)
        rhs = instance.q_cu_beta[i].value*u*instance.reclmtd_cu_beta[i].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq31_results[i] = local_result

    feas_results['eq31'] = eq31_results

def check_eq32_feasibility(instance, feas_results):
    eq32_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.area_hu_beta[j].value
        u = pow(1/instance.Hc[j] + 1/instance.H_hu, instance.Beta)
        rhs = instance.q_hu_beta[j].value*u*instance.reclmtd_hu_beta[j].value
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq32_results[j] = local_result

    feas_results['eq32'] = eq32_results

# q_beta (not in synheat model)
def check_eq33_feasibility(instance, feas_results):
    eq33_results = {}
    for i in instance.HP:
        for j in instance.CP:
            for k in instance.ST:
                local_result = {}
                lhs = instance.q_beta[i,j,k].value
                if instance.q[i,j,k].value < 0:
                    rhs = 0
                else:
                    rhs = pow(instance.q[i,j,k].value, instance.Beta)
                eps = rhs - lhs
                local_result['lhs'] = lhs
                local_result['rhs'] = rhs
                local_result['eps'] = eps
                eq33_results[(i,j,k)] = local_result
    feas_results['eq33'] = eq33_results

def check_eq34_feasibility(instance, feas_results):
    eq34_results = {}
    for i in instance.HP:
        local_result = {}
        lhs = instance.q_cu_beta[i].value
        if instance.q_cu[i].value < 0:
            rhs = 0
        else:
            rhs = pow(instance.q_cu[i].value, instance.Beta)
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq34_results[i] = local_result
    feas_results['eq34'] = eq34_results

def check_eq35_feasibility(instance, feas_results):
    eq35_results = {}
    for j in instance.CP:
        local_result = {}
        lhs = instance.q_hu_beta[j].value
        if instance.q_hu[j].value < 0:
            rhs = 0
        else:
            rhs = pow(instance.q_hu[j].value, instance.Beta)
        eps = rhs - lhs
        local_result['lhs'] = lhs
        local_result['rhs'] = rhs
        local_result['eps'] = eps
        eq35_results[j] = local_result
    feas_results['eq35'] = eq35_results

def check_feasibility(instance):
    feas_results = {}
    check_eq1_feasibility(instance, feas_results)
    check_eq2_feasibility(instance, feas_results)
    check_eq3_feasibility(instance, feas_results)
    check_eq4_feasibility(instance, feas_results)
    check_eq5_feasibility(instance, feas_results)
    check_eq6_feasibility(instance, feas_results)
    check_eq7_feasibility(instance, feas_results)
    check_eq8_feasibility(instance, feas_results)
    check_eq9_feasibility(instance, feas_results)
    check_eq10_feasibility(instance, feas_results)
    check_eq11_feasibility(instance, feas_results)
    check_eq12_feasibility(instance, feas_results)
    check_eq13_feasibility(instance, feas_results)
    check_eq14_feasibility(instance, feas_results)
    check_eq15_feasibility(instance, feas_results)
    check_eq16_feasibility(instance, feas_results)
    check_eq17_feasibility(instance, feas_results)
    check_eq18_feasibility(instance, feas_results)
    check_eq19_feasibility(instance, feas_results)
    check_eq20_feasibility(instance, feas_results)
    check_eq21_feasibility(instance, feas_results)
    check_eq22_feasibility(instance, feas_results)
    check_eq23_feasibility(instance, feas_results)
    check_eq24_feasibility(instance, feas_results)
    check_eq25_feasibility(instance, feas_results)
    check_eq26_feasibility(instance, feas_results)
    check_eq27_feasibility(instance, feas_results)
    check_eq28_feasibility(instance, feas_results)
    check_eq29_feasibility(instance, feas_results)
    check_eq30_feasibility(instance, feas_results)
    check_eq31_feasibility(instance, feas_results)
    check_eq32_feasibility(instance, feas_results)
    check_eq33_feasibility(instance, feas_results)
    check_eq34_feasibility(instance, feas_results)
    check_eq35_feasibility(instance, feas_results)

    return feas_results

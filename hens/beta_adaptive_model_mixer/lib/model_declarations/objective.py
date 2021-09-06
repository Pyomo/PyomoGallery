# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from pyomo.core.base.objective import Objective

def TAC_rule(model):
    total_cu_load = sum( model.q_cu[i] for i in model.HP )
    total_hu_load = sum( model.q_hu[j] for j in model.CP )

    total_number_of_stream_hx = sum( model.z[i,j,k] for i in model.HP for j in model.CP for k in model.ST )
    total_number_of_cu_hx  = sum( model.z_cu[i]  for i in model.HP )
    total_number_of_hu_hx  = sum( model.z_hu[j]  for j in model.CP )
    total_number_of_hx     = total_number_of_stream_hx + total_number_of_cu_hx + total_number_of_hu_hx

    total_area_of_stream_hx = sum( model.area_beta[i,j,k] for i in model.HP for j in model.CP for k in model.ST )
    total_area_of_cu_hx  = sum( model.area_cu_beta[i]  for i in model.HP )
    total_area_of_hu_hx  = sum( model.area_hu_beta[j]  for j in model.CP )
    total_area_of_hx     = total_area_of_stream_hx + total_area_of_cu_hx + total_area_of_hu_hx

    return model.Cost_cu*total_cu_load + model.Cost_hu*total_hu_load + model.Cost_hx*total_number_of_hx + model.Alpha*total_area_of_hx

def declare_objective(model):
    model.TAC = Objective(rule=TAC_rule)

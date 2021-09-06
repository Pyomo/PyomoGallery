# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from pyomo.core.base.var import Var
from pyomo.core.base.set_types import Binary, NonNegativeReals

from .bound_generators import *
from .index_generators import *

############################################################
############################################################
################### Assignment Functions ###################
############################################################
############################################################
def declare_variables(model):
    model.area_beta    = Var(model.HP, model.CP, model.ST, initialize = 0, domain=NonNegativeReals)
    model.area_cu_beta = Var(model.HP, initialize = 0, domain=NonNegativeReals)
    model.area_hu_beta = Var(model.CP, initialize = 0, domain=NonNegativeReals)

    # Flow rates
    model.fh = Var(model.HP, model.CP, model.ST, bounds=fh_bounds,\
            doc="Flow rate entering heat exchanger ijk cold side" )
    model.fc = Var(model.HP, model.CP, model.ST, bounds=fc_bounds,\
            doc="Flow rate entering heat exchanger ijk hot side"  )

    # Per exchanger outlet
    model.thx = Var(model.HP, model.CP, model.ST, bounds=thx_bounds,\
            doc="Outlet temperature of the heat exchanger ijk hot side"  )
    model.tcx = Var(model.HP, model.CP, model.ST, bounds=tcx_bounds,\
            doc="Outlet temperature of the heat exchanger ijk cold side" )

    # Temperature approaches
    model.dt    = Var(model.HP, model.CP, model.K, bounds=dt_bounds,\
            doc="Approach between i and j in location k"  )
    model.dt_cu = Var(model.HP,                    bounds=dt_cu_bounds,\
            doc="Approach between i and the cold utility" )
    model.dt_hu = Var(model.CP,                    bounds=dt_hu_bounds,\
            doc="Approach between j and the hot utility"  )

    # Log mean temperature differences raised to the beta-th power
    model.reclmtd_beta = Var(model.HP, model.CP, model.ST,  bounds=reclmtd_beta_bounds,\
            doc="Log mean temperature difference between hot stream i and cold stream j at stage k raised to the beta-th power")
    model.reclmtd_cu_beta = Var(model.HP,                   bounds=reclmtd_cu_beta_bounds,\
            doc="Log mean temperature difference between hot stream i and cold utility raised to the beta-th power")
    model.reclmtd_hu_beta = Var(model.CP,                   bounds=reclmtd_hu_beta_bounds,\
            doc="Log mean temperature difference between cold stream j and hot utility raised to the beta-th power")

    # Heat loads
    model.q    = Var(model.HP, model.CP, model.ST, bounds=q_bounds, initialize = 0,\
            doc="heat load between hot stream i and cold stream j at stage k" )
    model.q_cu = Var(model.HP,                     bounds=q_cu_bounds, initialize = 0,\
            doc="heat load between hot stream i and cold utility"             )
    model.q_hu = Var(model.CP,                     bounds=q_hu_bounds, initialize = 0,\
            doc="heat load between cold stream j and hot utility"             )

    # Heat loads to the beta-th power
    model.q_beta    = Var(model.HP, model.CP, model.ST, bounds=q_beta_bounds, initialize = 0,\
            doc="heat load between hot stream i and cold stream j at stage k raised to the beta-th power" )
    model.q_cu_beta = Var(model.HP,                     bounds=q_cu_beta_bounds, initialize = 0,\
            doc="heat load between hot stream i and cold utility raised to the beta-th power"             )
    model.q_hu_beta = Var(model.CP,                     bounds=q_hu_beta_bounds, initialize = 0,\
            doc="heat load between cold stream j and hot utility raised to the beta-th power"             )

    # Per stage temperatures
    model.th = Var(model.HP, model.K, bounds=th_bounds,\
            doc="temperature of hot stream i at hot end of stage k"  )
    model.tc = Var(model.CP, model.K, bounds=tc_bounds,\
            doc="temperature of cold stream j at hot end of stage k" )

    # Binary variables
    model.z    = Var(model.HP, model.CP, model.ST, initialize = 0, domain=Binary,\
            doc="existence of the match between hot stream i and cold stream j at stage k" )
    model.z_cu = Var(model.HP,                     initialize = 0, domain=Binary,\
            doc="existence of the match between hot stream i and cold utility"             )
    model.z_hu = Var(model.CP,                     initialize = 0, domain=Binary,\
            doc="existence of the match between cold stream j and hot utility"             )

    model.z_q_beta   = Var(z_q_beta_index, domain=Binary)
    model.z_q_cu_beta = Var(z_q_cu_beta_index, domain=Binary)
    model.z_q_hu_beta = Var(z_q_hu_beta_index, domain=Binary)

    model.z_area_beta_q = Var(z_area_beta_q_index, domain=Binary)
    model.z_area_beta_q_cu = Var(z_area_beta_q_cu_index, domain=Binary)
    model.z_area_beta_q_hu = Var(z_area_beta_q_hu_index, domain=Binary)

    model.var_delta_reclmtd_beta = Var(z_area_beta_q_index, domain=NonNegativeReals)
    model.var_delta_reclmtd_cu_beta = Var(z_area_beta_q_cu_index, domain=NonNegativeReals)
    model.var_delta_reclmtd_hu_beta = Var(z_area_beta_q_hu_index, domain=NonNegativeReals)

    # New variables
    model.bh_in  = Var(model.HP, model.CP, model.ST,  bounds=bh_bounds)
    model.bh_out = Var(model.HP, model.CP, model.ST,  bounds=bh_bounds)
    model.bc_in  = Var(model.HP, model.CP, model.ST,  bounds=bc_bounds)
    model.bc_out = Var(model.HP, model.CP, model.ST,  bounds=bc_bounds)

    model.z_th   = Var(z_th_index,  domain=Binary)
    model.z_thx  = Var(z_thx_index, domain=Binary)
    model.z_tc   = Var(z_tc_index,  domain=Binary)
    model.z_tcx  = Var(z_tcx_index, domain=Binary)

    model.var_delta_fh  = Var(var_delta_fh_index,  domain=NonNegativeReals)
    model.var_delta_fhx = Var(var_delta_fhx_index, domain=NonNegativeReals)
    model.var_delta_fc  = Var(var_delta_fc_index,  domain=NonNegativeReals)
    model.var_delta_fcx = Var(var_delta_fcx_index, domain=NonNegativeReals)

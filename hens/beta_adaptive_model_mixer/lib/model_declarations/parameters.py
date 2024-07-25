# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from pyomo.core.base.param import Param
from pyomo.core.base.sets import Set
from pyomo.core.base.rangeset import RangeSet
from pyomo.core.base.set_types import PositiveReals, NonNegativeReals, PositiveIntegers, PercentFraction

from .parameter_initialisation_functions import *

############################################################
############################################################
################### Assignment Functions ###################
############################################################
############################################################
def declare_parameters(model):
    model.Alpha       = Param(within=NonNegativeReals, doc="factor for area cost"                            )
    model.Beta        = Param(within=PercentFraction , doc="exponent for the area cost"                      )
    model.Cost_hx  = Param(within=NonNegativeReals, doc="fixed charge for exchangers"                     )
    model.Cost_cu     = Param(within=NonNegativeReals, doc="utility cost coeffiecient for cooling utility j" )
    model.Cost_hu     = Param(within=NonNegativeReals, doc="utility cost coeffiecient for heating utility k" )
    model.Delta_t_min = Param(within=NonNegativeReals, doc="minimum temperature approach"                    )

    model.Number_stages      = Param(within=PositiveIntegers, doc="number of stages"       )
    model.Number_hot_stream  = Param(within=PositiveIntegers, doc="number of hot streams"  )
    model.Number_cold_stream = Param(within=PositiveIntegers, doc="number of cold streams" )

    model.First_stage = Param(within=PositiveIntegers, default=1,                    doc='Index of the first stage')
    model.Last_stage  = Param(within=PositiveIntegers, default=model.Number_stages+1, doc='Index of the last stage' )

    model.HP = RangeSet(1, model.Number_hot_stream,  doc="set of hot process streams i"          )
    model.CP = RangeSet(1, model.Number_cold_stream, doc="set of cold process streams j"         )
    model.ST = RangeSet(model.First_stage, model.Number_stages,      doc="set of stages in the superstructure" )
    model.K  = RangeSet(model.First_stage, model.Last_stage, doc="set of temperature locations"          )
    model.First_Stage_Set = RangeSet(model.First_stage, model.First_stage)
    model.K_Take_First_Stage = model.K - model.First_Stage_Set

    model.Fh = Param(model.HP, doc="flow capicity of hot stream i"  )
    model.Fc = Param(model.CP, doc="flow capacity of cold stream j" )

    model.Hh   = Param(model.HP, doc="heat transfer coefficient for hot stream i"  )
    model.Hc   = Param(model.CP, doc="heat transfer coefficient for cold stream j" )
    model.H_cu = Param(          doc="heat transfer coefficient for cold utility"  )
    model.H_hu = Param(          doc="heat transfer coefficient for hot utility"   )

    model.Th_in  = Param(model.HP, doc="inlet temperature of hot stream i"   )
    model.Tc_in  = Param(model.CP, doc="inlet temperature of cold stream j"  )
    model.Th_out = Param(model.HP, doc="outlet temperature of hot stream i"  )
    model.Tc_out = Param(model.CP, doc="outlet temperature of cold stream j" )

    model.T_cu_in  = Param(within=PositiveReals, doc="inlet temperature of cold utility"  )
    model.T_cu_out = Param(within=PositiveReals, doc="outlet temperature of cold utility" )
    model.T_hu_in  = Param(within=PositiveReals, doc="inlet temperature of hot utility"   )
    model.T_hu_out = Param(within=PositiveReals, doc="outlet temperature of hot utility"  )

    ###############################
    #   Initialised Parameters    #
    ###############################
    model.Reclmtd_beta_gradient_points = Set(model.HP, model.CP, model.ST, dimen=2, initialize=[])
    model.Reclmtd_cu_beta_gradient_points = Set(model.HP, dimen=1, initialize=[])
    model.Reclmtd_hu_beta_gradient_points = Set(model.CP, dimen=1, initialize=[])

    model.U    = Param(model.HP, model.CP, within=PositiveReals, initialize=u_init)
    model.U_cu = Param(model.HP,           within=PositiveReals, initialize=u_cu_init)
    model.U_hu = Param(model.CP,           within=PositiveReals, initialize=u_hu_init)

    model.U_beta = Param(model.HP, model.CP, within=PositiveReals, initialize=u_beta_init)
    model.U_cu_beta = Param(model.HP, within=PositiveReals, initialize=u_cu_beta_init)
    model.U_hu_beta = Param(model.CP, within=PositiveReals, initialize=u_hu_beta_init)

    model.Ech = Param(model.HP, within=PositiveReals, initialize=ech_init)
    model.Ecc = Param(model.CP, within=PositiveReals, initialize=ecc_init)

    model.Omega_ij = Param(model.HP, model.CP, within=PositiveReals, initialize=omega_ij_init)
    model.Omega_i  = Param(model.HP,           within=PositiveReals, initialize=omega_i_init)
    model.Omega_j  = Param(model.CP,           within=PositiveReals, initialize=omega_j_init)

    model.Gamma = Param(model.HP, model.CP, within=NonNegativeReals, initialize=gamma_init)

    model.Th_breakpoints = Set(model.HP, model.ST, dimen=1, ordered=True, initialize=lambda model, i, k: th_breakpoints_init(model, i))

    model.Thx_breakpoints = Set(model.HP, model.CP, model.ST, dimen=1, ordered=True, initialize=lambda model, i, j, k: thx_breakpoints_init(model, i, j, k))

    model.Tc_breakpoints = Set(model.CP, model.K_Take_First_Stage, dimen=1, ordered=True, initialize=lambda model, j, k: tc_breakpoints_init(model, j))

    model.Tcx_breakpoints = Set(model.HP, model.CP, model.ST, dimen=1, ordered=True, initialize=lambda model, i, j, k: tcx_breakpoints_init(model, i, j, k))

    model.Q_beta_breakpoints = Set(model.HP, model.CP, model.ST, dimen=1, ordered=True,
        initialize=lambda model, i, j, k: q_beta_breakpoints_init(model, i, j))
    model.Q_beta_exp = Set(model.HP, model.CP, model.ST, dimen=1, ordered=True, \
        initialize=lambda model, i, j, k: map(lambda q: pow(q, model.Beta), model.Q_beta_breakpoints[i,j,k]))
    model.Q_beta_gradients = Set(model.HP, model.CP, model.ST, dimen=1, ordered=True, \
        initialize=q_beta_gradients_init)

    model.Q_cu_beta_breakpoints = Set(model.HP, dimen=1, ordered=True, \
        initialize=lambda model, i: q_cu_beta_breakpoints_init(model, i))
    model.Q_cu_beta_exp = Set(model.HP, dimen=1, ordered=True, \
        initialize=lambda model, i: map(lambda q: pow(q, model.Beta), model.Q_cu_beta_breakpoints[i]))
    model.Q_cu_beta_gradients = Set(model.HP, dimen=1, ordered=True, \
        initialize=q_cu_beta_gradients_init)

    model.Q_hu_beta_breakpoints = Set(model.CP, dimen=1, ordered=True, \
        initialize=lambda model, j: q_hu_beta_breakpoints_init(model, j))
    model.Q_hu_beta_exp = Set(model.CP, dimen=1, ordered=True, \
        initialize=lambda model, j: map(lambda q: pow(q, model.Beta), model.Q_hu_beta_breakpoints[j]))
    model.Q_hu_beta_gradients = Set(model.CP, dimen=1, ordered=True, \
        initialize=q_hu_beta_gradients_init)

    model.Area_beta_q_breakpoints = Set(model.HP, model.CP, model.ST, dimen=1, ordered=True, initialize=lambda model, i, j, k: area_beta_q_breakpoints_init(model, i, j))
    model.Area_beta_q_cu_breakpoints = Set(model.HP, dimen=1, ordered=True, initialize=lambda model, i: area_beta_q_cu_breakpoints_init(model, i))
    model.Area_beta_q_hu_breakpoints = Set(model.CP, dimen=1, ordered=True, initialize=lambda model, j: area_beta_q_hu_breakpoints_init(model, j))

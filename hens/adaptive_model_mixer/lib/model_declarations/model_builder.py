# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from pyomo.core.base.PyomoModel import AbstractModel
from pyomo.core.base.sets import Set

from .parameters  import declare_parameters
from .variables   import declare_variables
from .objective   import declare_objective
from .constraints import declare_constraints

def create_model():
    model = AbstractModel()
    declare_parameters(model)
    declare_variables(model)
    declare_objective(model)
    declare_constraints(model)
    return model

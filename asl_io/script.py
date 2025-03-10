#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2015-2025
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________


from pyomo.environ import *
from pyomo.opt import SolverFactory, TerminationCondition

def create_model():
    model = ConcreteModel()
    model.x = Var()
    model.o = Objective(expr=model.x)
    model.c = Constraint(expr=model.x >= 1)
    model.x.set_value(1.0)
    return model

if __name__ == "__main__":

    with SolverFactory("ipopt") as opt:
        model = create_model()
        results = opt.solve(model, load_solutions=False)
        if results.solver.termination_condition != TerminationCondition.optimal:
            raise RuntimeError('Solver did not report optimality:\n%s'
                               % (results.solver))
        model.solutions.load_from(results)
        print("Objective: %s" % (model.o()))

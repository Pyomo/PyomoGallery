from pyomo.environ import *
import random

random.seed(1000)

model = AbstractModel()

# Number of candidate locations
model.m = Param(within=PositiveIntegers)
# Number of customers
model.n = Param(within=PositiveIntegers)
# Set of candidate locations
model.M = RangeSet(1,model.m)
# Set of customer nodes
model.N = RangeSet(1,model.n)

# Number of facilities
model.p = Param(within=RangeSet(1,model.n))
# d[j] - demand of customer j
model.d = Param(model.N, default=1.0)
# c[i,j] - unit cost of satisfying customer j from facility i
model.c = Param(model.M, model.N, initialize=lambda i, j, model : random.uniform(1.0,2.0), within=Reals)

# x[i,j] - fraction of the demand of customer j that is supplied by facility i
model.x = Var(model.M, model.N, bounds=(0.0,1.0))
# y[i] - a binary value that is 1 is a facility is located at location i
model.y = Var(model.M, within=Binary)

# Minimize the demand-weighted total cost
def cost_(model):
    return sum(model.d[j]*model.c[i,j]*model.x[i,j] for i in model.M for j in model.N)
model.cost = Objective(rule=cost_)

# All of the demand for customer j must be satisfied
def demand_(model, j):
    return sum(model.x[i,j] for i in model.M) == 1.0
model.demand = Constraint(model.N, rule=demand_)

# Exactly p facilities are located
def facilities_(model):
    return sum(model.y[i] for i in model.M) == model.p
model.facilities = Constraint(rule=facilities_)

# Demand nodes can only be assigned to open facilities 
def openfac_(model, i, j):
    return model.x[i,j] <= model.y[i]
model.openfac = Constraint(model.M, model.N, rule=openfac_)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
from pyomo.environ import *
 
# Creation of a Concrete Model
model = ConcreteModel()
 

#  Set i, hours
model.i = Set(initialize=['1','2','3','4','5','6','7','8','9','10',
                          '11','12','13','14','15','16','17','18','19',
                          '20','21','22','23','24'], doc='Hours')                       
#  Set k, tasks
model.k = Set(initialize=['reaction', 'inject', 'cool', 'mix', 'package', 'collide', 'melt'], doc='Tasks')

#  Set m, materials
model.m = Set(initialize=['Plastic_Parts', 'Putty', 'ChemA', 'ChemB', 'Dark_Matter', 'Yogurt_Cups', 'Heat_Cool'], doc='Materials')


#Set materials_to_hours
def init_materials_to_hours(model):
    return (m+"-"+i for m in model.m for i in model.i)
model.materials_to_hours = Set(dimen=1,initialize=init_materials_to_hours) 
print "Materials to Hours Set"
#model.materials_to_hours.pprint()

#Set tasks_to_hours
def init_tasks_to_hours(model):
    return (k+"-"+i for k in model.k for i in model.i)
model.tasks_to_hours = Set(dimen=1,initialize=init_tasks_to_hours) 
print "Tasks to Hours Set"
#model.tasks_to_hours.pprint()

#Bounds on Decision Variables - Prevents schedule overrun
def DecBounds(model, i):
    isp = i.split("-")
    ii = int( isp[1] )
    ina = isp[0]
    
    if ina == "Plastic_Parts" and ii > (24-5): return (0,0)
    if ina == "Putty" and ii > (24-2): return (0,0)
    if ina == "ChemA" and ii > (24-4): return (0,0)
    if ina == "ChemB" and ii > (24-8): return (0,0)
    if ina == "Dark_Matter" and ii > (24-5): return (0,0)
    if ina == "Yogurt_Cups" and ii > (24-4): return (0,0)
    if ina == "Heat_Cool" and ii > (24-7): return (0,0)
    
    return (0,1)
#Binary Decision Variables Deci
def zeros(model, x):
   return 0
model.Deci = Var(model.materials_to_hours, within=Binary, initialize=zeros, bounds=DecBounds) 
model.Deci.pprint()
 
#Free Variables Task_HRS
model.Task_HRS = Var(model.tasks_to_hours, domain=NonNegativeIntegers) 
model.Task_HRS.pprint()
 
#Free Variables Resources
model.Resources = Var(model.k, domain=PositiveIntegers) 
model.Resources.pprint()

def mixer_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["mix-1"] == model.Resources['mix'] \
        - model.Deci["Putty-1"] - model.Deci["ChemB-1"]
    if ii == 2:
        return model.Task_HRS["mix-2"] == model.Task_HRS["mix-1"] \
        - model.Deci["Putty-2"] \
        - model.Deci["ChemB-2"] + model.Deci["ChemB-1"]  
    if ii == 3:
        return model.Task_HRS["mix-3"] == model.Task_HRS["mix-2"] \
        - model.Deci["Putty-3"] + model.Deci["Putty-1"] \
        - model.Deci["ChemB-3"] + model.Deci["ChemB-2"] \
        - model.Deci["Dark_Matter-1"]
    
    return model.Task_HRS["mix-"+i] == model.Task_HRS["mix-"+str(ii-1)] \
    - model.Deci["Putty-"+i] + model.Deci["Putty-"+str(ii-2)] \
    - model.Deci["ChemB-"+i] + model.Deci["ChemB-"+str(ii-1)] \
    - model.Deci["Dark_Matter-"+str(ii-2)] + model.Deci["Dark_Matter-"+str(ii-3)]   

model.mixer_constraint = Constraint(model.i, rule=mixer_rule)

def melter_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["melt-1"] == model.Resources['melt'] \
        - model.Deci["Plastic_Parts-1"] - model.Deci["ChemA-1"] \
        - model.Deci["Yogurt_Cups-1"] - model.Deci["Heat_Cool-1"]
    if ii > 1 and ii < 4: 
        return model.Task_HRS["melt-"+i] == model.Task_HRS["melt-"+str(ii-1)] \
        - model.Deci["Plastic_Parts-"+i] + model.Deci["Plastic_Parts-"+str(ii-1)] \
        - model.Deci["ChemA-"+i] + model.Deci["ChemA-"+str(ii-1)] \
        - model.Deci["Yogurt_Cups-"+i] + model.Deci["Yogurt_Cups-"+str(ii-1)] \
        - model.Deci["Heat_Cool-"+i] + model.Deci["Heat_Cool-"+str(ii-1)]       
    
    return model.Task_HRS["melt-"+i] == model.Task_HRS["melt-"+str(ii-1)] \
    - model.Deci["Plastic_Parts-"+i] + model.Deci["Plastic_Parts-"+str(ii-1)] \
    - model.Deci["ChemA-"+i] + model.Deci["ChemA-"+str(ii-1)] \
    - model.Deci["Yogurt_Cups-"+i] + model.Deci["Yogurt_Cups-"+str(ii-1)] \
    - model.Deci["Heat_Cool-"+i] + model.Deci["Heat_Cool-"+str(ii-1)] \
    - model.Deci["Heat_Cool-"+str(ii-2)] + model.Deci["Heat_Cool-"+str(ii-3)]   
    
model.melter_constraint = Constraint(model.i, rule=melter_rule)

def injector_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["inject-1"] == model.Resources['inject']
    if ii == 2:
        return model.Task_HRS["inject-2"] == model.Task_HRS["inject-1"] - model.Deci["Plastic_Parts-1"]
    if ii == 3:
        return model.Task_HRS["inject-3"] == model.Task_HRS["inject-2"] - model.Deci["Plastic_Parts-2"]        
    if ii > 3 and ii < 6:
        return model.Task_HRS["inject-"+i] == model.Task_HRS["inject-"+str(ii-1)] \
        - model.Deci["Plastic_Parts-"+str(ii-1)] \
        + model.Deci["Plastic_Parts-"+str(ii-3)]  
    return model.Task_HRS["inject-"+i] == model.Task_HRS["inject-"+str(ii-1)] \
    - model.Deci["Plastic_Parts-"+str(ii-1)] \
    + model.Deci["Plastic_Parts-"+str(ii-3)] \
    - model.Deci["Heat_Cool-"+str(ii-5)]        
    
model.injector_constraint = Constraint(model.i, rule=injector_rule)


def packager_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["package-1"] == model.Resources['package']
    if ii == 2:
        return model.Task_HRS["package-2"] == model.Task_HRS["package-1"] \
        - model.Deci["ChemA-1"] \
        - model.Deci["Yogurt_Cups-1"]
    if ii == 3:
        return model.Task_HRS["package-3"] == model.Task_HRS["package-2"] \
        - model.Deci["Putty-1"] \
        - model.Deci["ChemA-2"] \
        - model.Deci["Yogurt_Cups-2"]
    if ii > 3 and ii < 6:        
        return model.Task_HRS["package-"+i] == model.Task_HRS["package-"+str(ii-1)] \
        - model.Deci["Putty-"+str(ii-2)] + model.Deci["Putty-"+str(ii-3)] \
        - model.Deci["ChemA-"+str(ii-1)]  \
        - model.Deci["Yogurt_Cups-"+str(ii-1)]
    if ii > 5 and ii < 8:
        return model.Task_HRS["package-"+i] == model.Task_HRS["package-"+str(ii-1)] \
        - model.Deci["Putty-"+str(ii-2)] + model.Deci["Putty-"+str(ii-3)] \
        - model.Deci["Plastic_Parts-"+str(ii-5)] \
        - model.Deci["ChemA-"+str(ii-1)] + model.Deci["ChemA-"+str(ii-5)] \
        - model.Deci["Dark_Matter-"+str(ii-5)] \
        - model.Deci["Yogurt_Cups-"+str(ii-1)] + model.Deci["Yogurt_Cups-"+str(ii-5)] 
    if ii > 7 and ii < 9:
        return model.Task_HRS["package-"+i] == model.Task_HRS["package-"+str(ii-1)] \
        - model.Deci["Putty-"+str(ii-2)] + model.Deci["Putty-"+str(ii-3)] \
        - model.Deci["Plastic_Parts-"+str(ii-5)] + model.Deci["Plastic_Parts-"+str(ii-6)] \
        - model.Deci["ChemA-"+str(ii-1)] + model.Deci["ChemA-"+str(ii-5)] \
        - model.Deci["ChemB-"+str(ii-7)] \
        - model.Deci["Dark_Matter-"+str(ii-5)] + model.Deci["Dark_Matter-"+str(ii-6)] \
        - model.Deci["Yogurt_Cups-"+str(ii-1)] + model.Deci["Yogurt_Cups-"+str(ii-5)] \
        - model.Deci["Heat_Cool-"+str(ii-7)]  
    if ii > 8 and ii < 10: 
        return model.Task_HRS["package-"+i] == model.Task_HRS["package-"+str(ii-1)] \
        - model.Deci["Putty-"+str(ii-2)] + model.Deci["Putty-"+str(ii-3)] \
        - model.Deci["Plastic_Parts-"+str(ii-5)] + model.Deci["Plastic_Parts-"+str(ii-6)] \
        - model.Deci["ChemA-"+str(ii-1)] + model.Deci["ChemA-"+str(ii-5)] \
        - model.Deci["ChemB-"+str(ii-7)] \
        - model.Deci["Dark_Matter-"+str(ii-5)] + model.Deci["Dark_Matter-"+str(ii-6)] \
        - model.Deci["Yogurt_Cups-"+str(ii-1)] + model.Deci["Yogurt_Cups-"+str(ii-5)] \
        - model.Deci["Heat_Cool-"+str(ii-7)] + model.Deci["Heat_Cool-"+str(ii-8)]       
        
    return model.Task_HRS["package-"+i] == model.Task_HRS["package-"+str(ii-1)] \
    - model.Deci["Putty-"+str(ii-2)] + model.Deci["Putty-"+str(ii-3)] \
    - model.Deci["Plastic_Parts-"+str(ii-5)] + model.Deci["Plastic_Parts-"+str(ii-6)] \
    - model.Deci["ChemA-"+str(ii-1)] + model.Deci["ChemA-"+str(ii-5)] \
    - model.Deci["ChemB-"+str(ii-7)] + model.Deci["ChemB-"+str(ii-9)] \
    - model.Deci["Dark_Matter-"+str(ii-5)] + model.Deci["Dark_Matter-"+str(ii-6)] \
    - model.Deci["Yogurt_Cups-"+str(ii-1)] + model.Deci["Yogurt_Cups-"+str(ii-5)] \
    - model.Deci["Heat_Cool-"+str(ii-7)] + model.Deci["Heat_Cool-"+str(ii-8)]

model.packager_constraint = Constraint(model.i, rule=packager_rule)

def collider_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["collide-1"] == model.Resources['collide'] - model.Deci["Dark_Matter-1"]
    if ii == 2:
        return model.Task_HRS["collide-2"] == model.Task_HRS["collide-1"] - model.Deci["Dark_Matter-2"]
        
    return model.Task_HRS["collide-"+i] == model.Task_HRS["collide-"+str(ii-1)] \
       - model.Deci["Dark_Matter-"+str(ii)] + model.Deci["Dark_Matter-"+str(ii-2)]   

model.collider_constraint = Constraint(model.i, rule=collider_rule)

def cooler_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["cool-1"] == model.Resources['cool']
    if ii == 2:
        return model.Task_HRS["cool-1"] == model.Task_HRS["cool-1"] - model.Deci["Heat_Cool-1"]      
    if ii == 3: 
        return model.Task_HRS["cool-"+i] == model.Task_HRS["cool-"+str(ii-1)] \
        - model.Deci["Heat_Cool-"+str(ii-1)] + model.Deci["Heat_Cool-"+str(ii-2)] 
    if ii == 4: 
        return model.Task_HRS["cool-"+i] == model.Task_HRS["cool-"+str(ii-1)] \
        - model.Deci["Plastic_Parts-"+str(ii-3)] \
        - model.Deci["Heat_Cool-"+str(ii-1)] + model.Deci["Heat_Cool-"+str(ii-2)] \
        - model.Deci["Heat_Cool-"+str(ii-3)]      
    if ii == 5: 
        return model.Task_HRS["cool-"+i] == model.Task_HRS["cool-"+str(ii-1)] \
        - model.Deci["Plastic_Parts-"+str(ii-3)] \
        - model.Deci["Dark_Matter-"+str(ii-4)]  \
        - model.Deci["Heat_Cool-"+str(ii-1)] + model.Deci["Heat_Cool-"+str(ii-2)] \
        - model.Deci["Heat_Cool-"+str(ii-3)] + model.Deci["Heat_Cool-"+str(ii-4)]
    if ii == 6:
        return model.Task_HRS["cool-"+i] == model.Task_HRS["cool-"+str(ii-1)] \
        - model.Deci["Plastic_Parts-"+str(ii-3)] + model.Deci["Plastic_Parts-"+str(ii-5)] \
        - model.Deci["Dark_Matter-"+str(ii-4)] + model.Deci["Dark_Matter-"+str(ii-5)] \
        - model.Deci["Heat_Cool-"+str(ii-1)] + model.Deci["Heat_Cool-"+str(ii-2)] \
        - model.Deci["Heat_Cool-"+str(ii-3)] + model.Deci["Heat_Cool-"+str(ii-4)]
    if ii == 7:
        return model.Task_HRS["cool-"+i] == model.Task_HRS["cool-"+str(ii-1)] \
        - model.Deci["Plastic_Parts-"+str(ii-3)] + model.Deci["Plastic_Parts-"+str(ii-5)] \
        - model.Deci["ChemB-"+str(ii-6)] \
        - model.Deci["Dark_Matter-"+str(ii-4)] + model.Deci["Dark_Matter-"+str(ii-5)] \
        - model.Deci["Heat_Cool-"+str(ii-1)] + model.Deci["Heat_Cool-"+str(ii-2)] \
        - model.Deci["Heat_Cool-"+str(ii-3)] + model.Deci["Heat_Cool-"+str(ii-4)]

    return model.Task_HRS["cool-"+i] == model.Task_HRS["cool-"+str(ii-1)] \
    - model.Deci["Plastic_Parts-"+str(ii-3)] + model.Deci["Plastic_Parts-"+str(ii-5)] \
    - model.Deci["ChemB-"+str(ii-6)] + model.Deci["ChemB-"+str(ii-7)] \
    - model.Deci["Dark_Matter-"+str(ii-4)] + model.Deci["Dark_Matter-"+str(ii-5)] \
    - model.Deci["Heat_Cool-"+str(ii-1)] + model.Deci["Heat_Cool-"+str(ii-2)] \
    - model.Deci["Heat_Cool-"+str(ii-3)] + model.Deci["Heat_Cool-"+str(ii-4)]
    
model.cooler_constraint = Constraint(model.i, rule=cooler_rule)

def reactor_rule(model, i):
    ii = int(i)
    if ii == 1:
        return model.Task_HRS["reaction-1"] == model.Resources['reaction']
    if ii > 1 and ii < 4:
        return model.Task_HRS["reaction-"+i] == model.Task_HRS["reaction-"+str(ii-1)] \
        - model.Deci["ChemB-"+str(ii-1)] 
    if ii > 3 and ii < 5:
        return model.Task_HRS["reaction-"+i] == model.Task_HRS["reaction-"+str(ii-1)] \
        - model.Deci["ChemB-"+str(ii-1)] \
        - model.Deci["Dark_Matter-"+str(ii-3)]    
    if ii > 4 and ii < 7:
        return model.Task_HRS["reaction-"+i] == model.Task_HRS["reaction-"+str(ii-1)] \
        - model.Deci["ChemB-"+str(ii-1)] \
        - model.Deci["Dark_Matter-"+str(ii-3)] + model.Deci["Dark_Matter-"+str(ii-4)]
        
    return model.Task_HRS["reaction-"+i] == model.Task_HRS["reaction-"+str(ii-1)] \
    - model.Deci["ChemB-"+str(ii-1)] + model.Deci["ChemB-"+str(ii-6)] \
    - model.Deci["Dark_Matter-"+str(ii-3)] + model.Deci["Dark_Matter-"+str(ii-4)]
    
model.reactor_constraint = Constraint(model.i, rule=reactor_rule)

#Objective
def objective_rule(model):
  return sum(model.Task_HRS[k+"-"+i] for k in model.k for i in model.i)
#return sum(model.resourceAllocation[i,j] for i in model.i for j in model.j)  
model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')
 
 
## Display of the output ##
# Display x.l, x.m ;
##def pyomo_postprocess(options=None, instance=None, results=None):
##  model.Deci.display()
##  model.Task_HRS.display()
 
# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == '__main__':
    # This emulates what the pyomo command-line tools does
    
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("cplex")
    results = opt.solve(model)
    #sends results to stdout

    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, instance, results)
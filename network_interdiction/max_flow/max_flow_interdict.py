import pandas
import pyomo
import pyomo.opt
import pyomo.environ as pe
import logging

class MaxFlowInterdiction:
    """A class to compute max-flow interdictions."""

    def __init__(self, nodefile, arcfile, attacks=0):
        """
        All the files are CSVs with columns described below.  Attacks is the number of attacks.

        - nodefile:
            Node

        Every node must appear as a line in the nodefile. There are two special nodes called 'Start' and 'End' that define the source and sink of the max-flow problem. 

        - arcfile:
            StartNode,EndNode,Capacity,Attackable

        Every arc must appear in the arcfile.  The data also describes the arc's capacity and whether we can attack this arc.
        """
        # Read in the node_data
        self.node_data = pandas.read_csv(nodefile)
        self.node_data.set_index(['Node'], inplace=True)
        self.node_data.sort_index(inplace=True)
        # Read in the arc_data
        self.arc_data = pandas.read_csv(arcfile)
        self.arc_data['xbar'] = 0
        self.arc_data.set_index(['StartNode','EndNode'], inplace=True)
        self.arc_data.sort_index(inplace=True)

        self.attacks = attacks
     
        self.node_set = self.node_data.index.unique()
        self.arc_set = self.arc_data.index.unique()
        
        self.createPrimal()
        self.createInterdictionDual()


    def createPrimal(self):  
        """Create the primal pyomo model.  
        
        This is used to compute flows after interdiction.  The interdiction is stored in arc_data.xbar."""

        model = pe.ConcreteModel()
        # Tell pyomo to read in dual-variable information from the solver
        model.dual = pe.Suffix(direction=pe.Suffix.IMPORT) 

        # Add the sets
        model.node_set = pe.Set( initialize=self.node_set )
        model.edge_set = pe.Set( initialize=self.arc_set, dimen=2)

        # Create the variables
        model.y = pe.Var(model.edge_set, domain=pe.NonNegativeReals) 
        model.v = pe.Var(domain=pe.NonNegativeReals)

        
        # Create the objective
        def obj_rule(model):
            return  model.v - 1.1*sum( data['xbar']*model.y[e] for e,data in self.arc_data.iterrows())
        model.OBJ = pe.Objective(rule=obj_rule, sense=pe.maximize)

        # Create the constraints, one for each node
        def flow_bal_rule(model, n):
            tmp = self.arc_data.reset_index()
            successors = tmp.ix[ tmp.StartNode == n, 'EndNode'].values
            predecessors = tmp.ix[ tmp.EndNode == n, 'StartNode'].values 
            lhs = sum(model.y[(i,n)] for i in predecessors) - sum(model.y[(n,i)] for i in successors) 
            start_node = int(n == 'Start')
            end_node = int(n == 'End')
            rhs = 0 - model.v*(start_node) + model.v*(end_node)
            constr = (lhs == rhs)
            if isinstance(constr, bool):
                return pe.Constraint.Skip
            return constr

        model.FlowBalance = pe.Constraint(model.node_set, rule=flow_bal_rule)
        
        # Capacity constraints, one for each edge
        def capacity_rule(model, i, j):
            capacity = self.arc_data['Capacity'].get((i,j),-1)
            if capacity < 0:
                return pe.Constraint.Skip
            return model.y[(i,j)] <= capacity 

        model.Capacity = pe.Constraint(model.edge_set, rule=capacity_rule)
 
        # Store the model
        self.primal = model

    def createInterdictionDual(self):
        # Create the model
        model = pe.ConcreteModel()
        
        # Add the sets
        model.node_set = pe.Set( initialize=self.node_set )
        model.edge_set = pe.Set( initialize=self.arc_set, dimen=2)

        # Create the variables
        model.rho = pe.Var(model.node_set, domain=pe.Reals)
        model.pi = pe.Var(model.edge_set, domain=pe.NonNegativeReals)
        
        model.x = pe.Var(model.edge_set, domain=pe.Binary)

        # Create the objective
        def obj_rule(model):
            return  sum(data['Capacity']*model.pi[e] for e,data in self.arc_data.iterrows() if data['Capacity']>=0)

        model.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)

        # Create the constraints for y_ij
        def edge_constraint_rule(model, i, j):
            attackable = int(self.arc_data['Attackable'].get((i,j),0))
            hasCap = int(self.arc_data['Capacity'].get((i,j),-1)>=0)
            return model.rho[j] - model.rho[i] + model.pi[(i,j)]*hasCap >=  0 - 1.1*model.x[(i,j)]*attackable

        model.DualEdgeConstraint = pe.Constraint(model.edge_set, rule=edge_constraint_rule)

        # Set the x's for non-blockable arcs
        def v_constraint_rule(model):
            return model.rho['Start'] - model.rho['End'] == 1

        model.VConstraint = pe.Constraint(rule=v_constraint_rule)
     
        # Create the interdiction budget constraint 
        def block_limit_rule(model):
            model.attacks = self.attacks
            return pe.summation(model.x) <= model.attacks

        model.BlockLimit = pe.Constraint(rule=block_limit_rule)

        # Create, save the model
        self.Idual = model

    def solve(self, tee=False):
        solver = pyomo.opt.SolverFactory('gurobi')

        # Solve the dual first
        self.Idual.BlockLimit.construct()
        self.Idual.BlockLimit._constructed = False
        del self.Idual.BlockLimit._data[None] 
        self.Idual.BlockLimit.reconstruct()
        self.Idual.preprocess()
        results = solver.solve(self.Idual, tee=tee, keepfiles=False, options_string="mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0")

        # Check that we actually computed an optimal solution, load results
        if (results.solver.status != pyomo.opt.SolverStatus.ok):
            logging.warning('Check solver not ok?')
        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):  
            logging.warning('Check solver optimality?')

        self.Idual.solutions.load_from(results)
        # Now put interdictions into xbar and solve primal
       
        for e in self.arc_data.index:
            self.arc_data.ix[e,'xbar'] = self.Idual.x[e].value

        self.primal.OBJ.construct()
        self.primal.OBJ._constructed = False
        self.primal.OBJ._init_sense = pe.maximize
        del self.primal.OBJ._data[None] 
        self.primal.OBJ.reconstruct()
        self.primal.preprocess()
        results = solver.solve(self.primal, tee=tee, keepfiles=False, options_string="mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0")

        # Check that we actually computed an optimal solution, load results
        if (results.solver.status != pyomo.opt.SolverStatus.ok):
            logging.warning('Check solver not ok?')
        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):  
            logging.warning('Check solver optimality?')

        self.primal.solutions.load_from(results)

    def printSolution(self):
        print()
        print('Using %d attacks:'%self.attacks)
        print()
        edges = sorted(self.arc_set)
        for e in edges:
            if self.Idual.x[e].value > 0:
                print('Interdict arc %s -> %s'%(str(e[0]), str(e[1])))
        print()
         
        for e0,e1 in self.arc_set:
            flow = self.primal.y[(e0,e1)].value
            if flow > 0:
                print('Flow on arc %s -> %s: %.2f'%(str(e0), str(e1), flow))
        print()

        print('----------')
        print('Total flow = %.2f (primal) %.2f (dual)'%(self.primal.OBJ(), self.Idual.OBJ()))


########################
# Now lets do something
########################

if __name__ == '__main__':
    m = MaxFlowInterdiction('sample_nodes_data.csv', 'sample_arcs_data.csv')
    m.solve()
    m.printSolution()
    m.attacks = 1
    m.solve()
    m.printSolution()
    m.attacks = 2
    m.solve()
    m.printSolution()

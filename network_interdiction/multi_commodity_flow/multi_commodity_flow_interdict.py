import pandas
import pyomo
import pyomo.opt
import pyomo.environ as pe
import logging

class MultiCommodityInterdiction:
    """A class to compute multicommodity flow interdictions."""

    def __init__(self, nodefile, node_commodity_file, arcfile, arc_commodity_file, attacks=0):
        """
        All the files are CSVs with columns described below.  Attacks is the number of attacks.

        - nodefile:
            Node

        Every node must appear as a line in the nodefile.  You can have additional columns as well.

        - node_commodity_file:
            Node,Commodity,SupplyDemand

        Every commodity node imbalance that is not zero must appear in the node_commodity_file

        - arcfile:
            StartNode,EndNode,Capacity,Attackable

        Every arc must appear in the arcfile.  Also the arcs total capacity and whether we can attack this arc.

        - arc_commodity_file:
            StartNode,EndNode,Commodity,Cost,Capacity

        This file specifies the costs and capacities of moving each commodity across each arc.  If an (node, node, commodity) tuple does not appear in this file, then it means the commodity cannot flow across that edge.
        """
        # Read in the node_data
        self.node_data = pandas.read_csv(nodefile)
        self.node_data.set_index(['Node'], inplace=True)
        self.node_data.sort_index(inplace=True)
        # Read in the node_commodity_data
        self.node_commodity_data = pandas.read_csv(node_commodity_file)
        self.node_commodity_data.set_index(['Node','Commodity'], inplace=True)
        self.node_commodity_data.sort_index(inplace=True)
        # Read in the arc_data
        self.arc_data = pandas.read_csv(arcfile)
        self.arc_data.set_index(['StartNode','EndNode'], inplace=True)
        self.arc_data.sort_index(inplace=True)
        # Read in the arc_commodity_data
        self.arc_commodity_data = pandas.read_csv(arc_commodity_file)
        self.arc_commodity_data['xbar'] = 0
        self.arc_commodity_data.set_index(['StartNode','EndNode','Commodity'], inplace=True)
        self.arc_commodity_data.sort_index(inplace=True)
        # Can df.reset_index() to go back

        self.attacks = attacks
     
        self.node_set = self.node_data.index.unique()
        self.commodity_set = self.node_commodity_data.index.levels[1].unique()
        self.arc_set = self.arc_data.index.unique()
        
        # Compute nCmax
        self.nCmax = len(self.node_set) * self.arc_commodity_data['Cost'].max()

        self.createPrimal()
        self.createInterdictionDual()


    def createPrimal(self):  
        """Create the primal pyomo model.  
        
        This is used to compute flows after interdiction.  The interdiction is stored in arc_commodity_data.xbar."""

        model = pe.ConcreteModel()
        # Tell pyomo to read in dual-variable information from the solver
        model.dual = pe.Suffix(direction=pe.Suffix.IMPORT) 

        # Add the sets
        model.node_set = pe.Set( initialize=self.node_set )
        model.edge_set = pe.Set( initialize=self.arc_set, dimen=2)
        model.commodity_set = pe.Set( initialize=self.commodity_set )

        # Create the variables
        model.y = pe.Var(model.edge_set*model.commodity_set, domain=pe.NonNegativeReals) 
        model.UnsatSupply = pe.Var(model.node_set*model.commodity_set, domain=pe.NonNegativeReals)
        model.UnsatDemand = pe.Var(model.node_set*model.commodity_set, domain=pe.NonNegativeReals)
        
        # Create the objective
        def obj_rule(model):
            return  sum( (data['Cost']+data['xbar']*(2*self.nCmax+1))*model.y[e] for e,data in self.arc_commodity_data.iterrows()) + sum(self.nCmax*(model.UnsatSupply[n] + model.UnsatDemand[n]) for n,data in self.node_commodity_data.iterrows())
        model.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)

        # Create the constraints, one for each node
        def flow_bal_rule(model, n,k):
            tmp = self.arc_data.reset_index()
            successors = tmp.ix[ tmp.StartNode == n, 'EndNode'].values
            predecessors = tmp.ix[ tmp.EndNode == n, 'StartNode'].values 
            lhs = sum(model.y[(i,n,k)] for i in predecessors) - sum(model.y[(n,i,k)] for i in successors) 
            imbalance = self.node_commodity_data['SupplyDemand'].get((n,k),0)
            supply_node = int(imbalance < 0)
            demand_node = int(imbalance > 0)
            rhs = (imbalance + model.UnsatSupply[n,k]*(supply_node) - model.UnsatDemand[n,k]*(demand_node))
            constr = (lhs == rhs)
            if isinstance(constr, bool):
                return pe.Constraint.Skip
            return constr

        model.FlowBalance = pe.Constraint(model.node_set*model.commodity_set, rule=flow_bal_rule)
        
        # Capacity constraints, one for each edge and commodity
        def capacity_rule(model, i, j, k):
            capacity = self.arc_commodity_data['Capacity'].get((i,j,k),-1)
            if capacity < 0:
                return pe.Constraint.Skip
            return model.y[(i,j,k)] <= capacity 

        model.Capacity = pe.Constraint(model.edge_set*model.commodity_set, rule=capacity_rule)
 
        # Joint capacity constraints, one for each edge
        def joint_capacity_rule(model, i, j):
            capacity = self.arc_data['Capacity'].get((i,j), -1)
            if capacity < 0:
                return pe.Constraint.Skip
            return sum(model.y[(i,j,k)] for k in self.commodity_set) <= capacity

        model.JointCapacity = pe.Constraint(model.edge_set, rule=joint_capacity_rule)

        # Store the model
        self.primal = model

    def createInterdictionDual(self):
        # Create the model
        model = pe.ConcreteModel()
        
        # Add the sets
        model.node_set = pe.Set( initialize=self.node_set )
        model.edge_set = pe.Set( initialize=self.arc_set, dimen=2)
        model.commodity_set = pe.Set( initialize=self.commodity_set )

        # Create the variables
        model.rho = pe.Var(model.node_set*model.commodity_set, domain=pe.Reals)
        model.piSingle = pe.Var(model.edge_set*model.commodity_set, domain=pe.NonPositiveReals)
        model.piJoint = pe.Var(model.edge_set, domain=pe.NonPositiveReals)
        
        model.x = pe.Var(model.edge_set, domain=pe.Binary)

        # Create the objective
        def obj_rule(model):
            return  sum(data['Capacity']*model.piJoint[e] for e,data in self.arc_data.iterrows() if data['Capacity']>=0) +\
                    sum(data['Capacity']*model.piSingle[e] for e,data in self.arc_commodity_data.iterrows() if data['Capacity']>=0)+\
                    sum(data['SupplyDemand']*model.rho[n] for n,data in self.node_commodity_data.iterrows())

        model.OBJ = pe.Objective(rule=obj_rule, sense=pe.maximize)

        # Create the constraints for y_ijk
        def edge_constraint_rule(model, i, j, k):
            if (i,j,k) not in self.arc_commodity_data.index:
                return pe.Constraint.Skip
            attackable = int(self.arc_data['Attackable'].get((i,j),0))
            hasSingleCap = int(self.arc_commodity_data['Capacity'].get((i,j,k),-1)>=0)
            hasJointCap = int(self.arc_data['Capacity'].get((i,j),-1)>=0)
            return model.rho[(j,k)] - model.rho[(i,k)] + model.piSingle[(i,j,k)]*hasSingleCap + model.piJoint[(i,j)]*hasJointCap <=  self.arc_commodity_data['Cost'].get((i,j,k)) + (2*self.nCmax+1)*model.x[(i,j)]*attackable

        model.DualEdgeConstraint = pe.Constraint(model.edge_set*model.commodity_set, rule=edge_constraint_rule)
        
        # Create constraints for the UnsatDemand variables 
        def unsat_constraint_rule(model, n, k):
            if (n,k) not in self.node_commodity_data.index:
                return pe.Constraint.Skip
            imbalance = self.node_commodity_data['SupplyDemand'].get((n,k),0)
            supply_node = int(imbalance < 0)
            demand_node = int(imbalance > 0)
            if (supply_node):
                return -model.rho[(n,k)] <= self.nCmax
            if (demand_node):
                return model.rho[(n,k)] <= self.nCmax
            return pe.Constraint.Skip

        model.UnsatConstraint = pe.Constraint(model.node_set*model.commodity_set, rule=unsat_constraint_rule)
     
        # Create the interdiction budget constraint 
        def block_limit_rule(model):
            model.attacks = self.attacks
            return pe.summation(model.x) <= model.attacks

        model.BlockLimit = pe.Constraint(rule=block_limit_rule)

        # Create, save the model
        self.Idual = model

    def solve(self, tee=False):
        solver = pyomo.opt.SolverFactory('cplex')

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
            self.arc_commodity_data.ix[e,'xbar'] = self.Idual.x[e].value

        self.primal.OBJ.construct()
        self.primal.OBJ._constructed = False
        self.primal.OBJ._init_sense = pe.minimize
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
        
        nodes = sorted(self.node_commodity_data.index)
        for n in nodes:
            remaining_supply = self.primal.UnsatSupply[n].value
            if remaining_supply > 0:
                print('Remaining supply of %s on node %s: %.2f'%(str(n[1]), str(n[0]), remaining_supply))
        for n in nodes:
            remaining_demand = self.primal.UnsatDemand[n].value
            if remaining_demand > 0:
                print('Remaining demand of %s on node %s: %.2f'%(str(n[1]), str(n[0]), remaining_demand))
        print()
        
        for e0,e1 in self.arc_set:
            for k in self.commodity_set:
                flow = self.primal.y[(e0,e1,k)].value
                if flow > 0:
                    print('Flow on arc %s -> %s: %.2f %s'%(str(e0), str(e1), flow, str(k)))
        print()

        print('----------')
        print('Total cost = %.2f (primal) %.2f (dual)'%(self.primal.OBJ(), self.Idual.OBJ()))


########################
# Now lets do something
########################

if __name__ == '__main__':
    m = MultiCommodityInterdiction('sample_nodes_data.csv', 'sample_nodes_commodity_data.csv', 'sample_arcs_data.csv', 'sample_arcs_commodity_data.csv')
    m.solve()
    m.printSolution()
    m.attacks = 1
    m.solve()
    m.printSolution()
    m.attacks = 2
    m.solve()
    m.printSolution()

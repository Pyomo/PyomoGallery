import pyomo
import pandas
import pyomo.opt
import pyomo.environ as pe

class MinCostFlow:
    """This class implements a standard min-cost-flow model.  
    
    It takes as input two csv files, providing data for the nodes and the arcs of the network.  The nodes file should have columns:
    
    Node, Imbalance

    that specify the node name and the flow imbalance at the node.  The arcs file should have columns:

    Start, End, Cost, UpperBound, LowerBound

    that specify an arc start node, an arc end node, a cost for the arc, and upper and lower bounds for the flow."""
    def __init__(self, nodesfile, arcsfile):
        """Read in the csv data."""
        # Read in the nodes file
        self.node_data = pandas.read_csv('nodes.csv')
        self.node_data.set_index(['Node'], inplace=True)
        self.node_data.sort_index(inplace=True)
        # Read in the arcs file
        self.arc_data = pandas.read_csv('arcs.csv')
        self.arc_data.set_index(['Start','End'], inplace=True)
        self.arc_data.sort_index(inplace=True)

        self.node_set = self.node_data.index.unique()
        self.arc_set = self.arc_data.index.unique()

        self.createModel()

    def createModel(self):
        """Create the pyomo model given the csv data."""
        self.m = pe.ConcreteModel()

        # Create sets
        self.m.node_set = pe.Set( initialize=self.node_set )
        self.m.arc_set = pe.Set( initialize=self.arc_set , dimen=2)

        # Create variables
        self.m.Y = pe.Var(self.m.arc_set, domain=pe.NonNegativeReals)

        # Create objective
        def obj_rule(m):
            return sum(m.Y[e] * self.arc_data.ix[e,'Cost'] for e in self.arc_set)
        self.m.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)
        
        # Flow Ballance rule
        def flow_bal_rule(m, n):
            arcs = self.arc_data.reset_index()
            preds = arcs[ arcs.End == n ]['Start']
            succs = arcs[ arcs.Start == n ]['End']
            return sum(m.Y[(p,n)] for p in preds) - sum(m.Y[(n,s)] for s in succs) == self.node_data.ix[n,'Imbalance']
        self.m.FlowBal = pe.Constraint(self.m.node_set, rule=flow_bal_rule)

        # Upper bounds rule
        def upper_bounds_rule(m, n1, n2):
            e = (n1,n2)
            if self.arc_data.ix[e, 'UpperBound'] < 0:
                return pe.Constraint.Skip
            return m.Y[e] <= self.arc_data.ix[e, 'UpperBound']
        self.m.UpperBound = pe.Constraint(self.m.arc_set, rule=upper_bounds_rule)
        
        # Lower bounds rule
        def lower_bounds_rule(m, n1, n2):
            e = (n1,n2)
            if self.arc_data.ix[e, 'LowerBound'] < 0:
                return pe.Constraint.Skip
            return m.Y[e] >= self.arc_data.ix[e, 'LowerBound']
        self.m.LowerBound = pe.Constraint(self.m.arc_set, rule=lower_bounds_rule)

    def solve(self):
        """Solve the model."""
        solver = pyomo.opt.SolverFactory('gurobi')
        results = solver.solve(self.m, tee=True, keepfiles=False, options_string="mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0")

        if (results.solver.status != pyomo.opt.SolverStatus.ok):
            logging.warning('Check solver not ok?')
        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):  
            logging.warning('Check solver optimality?') 


if __name__ == '__main__':
       sp = MinCostFlow('nodes.csv', 'arcs.csv') 
       sp.solve()
       print('\n\n---------------------------')
       print('Cost: ', sp.m.OBJ())

import pyomo
import pyomo.opt
import pyomo.environ as pe
import pandas
import networkx

class MSTRowGeneration:
    """A class to find Minimum Spanning Tree using a row-generation algorithm."""

    def __init__(self, nfile):
        """The input is a CSV file describing the undirected network's edges."""
        self.df = pandas.read_csv(nfile)

        self.createRelaxedModel()

    def createRelaxedModel(self):
        """Create the relaxed model, without any subtour elimination constraints."""
        df = self.df
        node_set = set( list( df.startNode ) + list(df.destNode) )

        # Create the model and sets
        m = pe.ConcreteModel()

        df.set_index(['startNode','destNode'], inplace=True)
        edge_set = df.index.unique()

        m.edge_set = pe.Set(initialize=edge_set, dimen=2)
        m.node_set = pe.Set(initialize=node_set)
    
        # Define variables
        m.Y = pe.Var(m.edge_set, domain=pe.Binary)

        # Objective
        def obj_rule(m):
            return sum( m.Y[e] * df.ix[e,'dist'] for e in m.edge_set)
        m.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)

        # Add the n-1 constraint
        def simple_const_rule(m):
            return sum( m.Y[e] for e in m.edge_set ) == len(node_set) - 1
        m.simpleConst = pe.Constraint(rule = simple_const_rule)
       
        # Empty constraint list for subtour elimination constraints
        # This is where the generated rows will go
        m.ccConstraints = pe.ConstraintList()

        self.m = m

    def convertYsToNetworkx(self):
        """Convert the model's Y variables into a networkx object."""
        ans = networkx.Graph()
        edges = [e for e in self.m.edge_set if self.m.Y[e].value > .99]
        ans.add_edges_from(edges)
        return ans

    def solve(self):
        """Solve for the MST, using row generation for subtour elimination constraints."""
        def createConstForCC(m, cc):
            cc = dict.fromkeys(cc)
            return sum( m.Y[e] for e in m.edge_set if ((e[0] in cc) and (e[1] in cc))) <= len(cc) - 1
        
        if not hasattr(self, 'solver'):
            solver = pyomo.opt.SolverFactory('gurobi')

        done = False
        while not done:
            # Solve once and add subtour elimination constraints if necessary
            # Finish when there are no more subtours
            results = solver.solve(self.m, tee=False, keepfiles=False, options_string="mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0")
            # Construct a graph from the answer, and look for subtours
            graph = self.convertYsToNetworkx()
            ccs = list(networkx.connected_component_subgraphs(graph))
            for cc in ccs:
                print('Adding constraint for connected component:')
                print(cc.nodes())
                print(createConstForCC(self.m, cc))
                print('--------------\n')
                self.m.ccConstraints.add( createConstForCC(self.m, cc) )
            if ccs[0].number_of_nodes() == len(self.m.node_set):
                done = True

mst = MSTRowGeneration('mst.csv')
mst.solve()

mst.m.Y.pprint()
print(mst.m.OBJ())

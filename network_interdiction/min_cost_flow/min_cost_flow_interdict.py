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


{
 "metadata": {
  "name": "",
  "signature": "sha256:3203a62c794b056e9202075c3d2f3cde57af44eeb452a1c3f9b1d52b52e69f8a"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "%load min_cost_flow_interdict.py"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 1
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "import networkx\n",
      "import pandas\n",
      "import pyomo\n",
      "import pyomo.opt\n",
      "import pyomo.environ as pe\n",
      "import scipy\n",
      "import itertools\n",
      "import logging\n",
      "\n",
      "class MinCostFlowInterdiction:\n",
      "    \"\"\"A class to compute min-cost-flow interdictions.\"\"\"\n",
      "\n",
      "    def __init__(self, nodefile, arcfile, attacks=0):\n",
      "        \"\"\"\n",
      "        All the files are CSVs with columns described below.  Attacks is the number of attacks.\n",
      "\n",
      "        - nodefile:\n",
      "            Node, SupplyDemand\n",
      "\n",
      "        Every node must appear as a line in the nodefile.  SupplyDemand describes the flow imbalance at the node.\n",
      "\n",
      "        - arcfile:\n",
      "            StartNode,EndNode,Capacity,Cost,Attackable\n",
      "\n",
      "        Every arc must appear in the arcfile.  The data also describes the arc's capacity, cost, and whether we can attack this arc.\n",
      "        \"\"\"\n",
      "        # Read in the node_data\n",
      "        self.node_data = pandas.read_csv(nodefile)\n",
      "        self.node_data.set_index(['Node'], inplace=True)\n",
      "        self.node_data.sort_index(inplace=True)\n",
      "        # Read in the arc_data\n",
      "        self.arc_data = pandas.read_csv(arcfile)\n",
      "        self.arc_data['xbar'] = 0\n",
      "        self.arc_data.set_index(['StartNode','EndNode'], inplace=True)\n",
      "        self.arc_data.sort_index(inplace=True)\n",
      "\n",
      "        self.attacks = attacks\n",
      "     \n",
      "        self.node_set = self.node_data.index.unique()\n",
      "        self.arc_set = self.arc_data.index.unique()\n",
      "        \n",
      "        # Compute nCmax\n",
      "        self.nCmax = len(self.node_set) * self.arc_data['Cost'].max()\n",
      "\n",
      "        self.createPrimal()\n",
      "        self.createInterdictionDual()\n",
      "\n",
      "\n",
      "    def createPrimal(self):  \n",
      "        \"\"\"Create the primal pyomo model.  \n",
      "        \n",
      "        This is used to compute flows after interdiction.  The interdiction is stored in arc_data.xbar.\"\"\"\n",
      "\n",
      "        model = pe.ConcreteModel()\n",
      "        # Tell pyomo to read in dual-variable information from the solver\n",
      "        model.dual = pe.Suffix(direction=pe.Suffix.IMPORT) \n",
      "\n",
      "        # Add the sets\n",
      "        model.node_set = pe.Set( initialize=self.node_set )\n",
      "        model.edge_set = pe.Set( initialize=self.arc_set, dimen=2)\n",
      "\n",
      "        # Create the variables\n",
      "        model.y = pe.Var(model.edge_set, domain=pe.NonNegativeReals) \n",
      "        model.UnsatSupply = pe.Var(model.node_set, domain=pe.NonNegativeReals)\n",
      "        model.UnsatDemand = pe.Var(model.node_set, domain=pe.NonNegativeReals)\n",
      "        \n",
      "        # Create the objective\n",
      "        def obj_rule(model):\n",
      "            return  sum( (data['Cost']+data['xbar']*(2*self.nCmax+1))*model.y[e] for e,data in self.arc_data.iterrows()) + sum(self.nCmax*(model.UnsatSupply[n] + model.UnsatDemand[n]) for n,data in self.node_data.iterrows())\n",
      "        model.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)\n",
      "\n",
      "        # Create the constraints, one for each node\n",
      "        def flow_bal_rule(model, n):\n",
      "            tmp = self.arc_data.reset_index()\n",
      "            successors = tmp.ix[ tmp.StartNode == n, 'EndNode'].values\n",
      "            predecessors = tmp.ix[ tmp.EndNode == n, 'StartNode'].values \n",
      "            lhs = sum(model.y[(i,n)] for i in predecessors) - sum(model.y[(n,i)] for i in successors) \n",
      "            imbalance = self.node_data['SupplyDemand'].get(n,0)\n",
      "            supply_node = int(imbalance < 0)\n",
      "            demand_node = int(imbalance > 0)\n",
      "            rhs = (imbalance + model.UnsatSupply[n]*(supply_node) - model.UnsatDemand[n]*(demand_node))\n",
      "            constr = (lhs == rhs)\n",
      "            if isinstance(constr, bool):\n",
      "                return pe.Constraint.Skip\n",
      "            return constr\n",
      "\n",
      "        model.FlowBalance = pe.Constraint(model.node_set, rule=flow_bal_rule)\n",
      "        \n",
      "        # Capacity constraints, one for each edge\n",
      "        def capacity_rule(model, i, j):\n",
      "            capacity = self.arc_data['Capacity'].get((i,j),-1)\n",
      "            if capacity < 0:\n",
      "                return pe.Constraint.Skip\n",
      "            return model.y[(i,j)] <= capacity \n",
      "\n",
      "        model.Capacity = pe.Constraint(model.edge_set, rule=capacity_rule)\n",
      " \n",
      "        # Store the model\n",
      "        self.primal = model\n",
      "\n",
      "    def createInterdictionDual(self):\n",
      "        # Create the model\n",
      "        model = pe.ConcreteModel()\n",
      "        \n",
      "        # Add the sets\n",
      "        model.node_set = pe.Set( initialize=self.node_set )\n",
      "        model.edge_set = pe.Set( initialize=self.arc_set, dimen=2)\n",
      "\n",
      "        # Create the variables\n",
      "        model.rho = pe.Var(model.node_set, domain=pe.Reals)\n",
      "        model.pi = pe.Var(model.edge_set, domain=pe.NonPositiveReals)\n",
      "        \n",
      "        model.x = pe.Var(model.edge_set, domain=pe.Binary)\n",
      "\n",
      "        # Create the objective\n",
      "        def obj_rule(model):\n",
      "            return  sum(data['Capacity']*model.pi[e] for e,data in self.arc_data.iterrows() if data['Capacity']>=0) +\\\n",
      "                    sum(data['SupplyDemand']*model.rho[n] for n,data in self.node_data.iterrows())\n",
      "\n",
      "        model.OBJ = pe.Objective(rule=obj_rule, sense=pe.maximize)\n",
      "\n",
      "        # Create the constraints for y_ij\n",
      "        def edge_constraint_rule(model, i, j):\n",
      "            attackable = int(self.arc_data['Attackable'].get((i,j),0))\n",
      "            hasCap = int(self.arc_data['Capacity'].get((i,j),-1)>=0)\n",
      "            return model.rho[j] - model.rho[i] + model.pi[(i,j)]*hasCap <=  self.arc_data['Cost'].get((i,j),0) + (2*self.nCmax+1)*model.x[(i,j)]*attackable\n",
      "\n",
      "        model.DualEdgeConstraint = pe.Constraint(model.edge_set, rule=edge_constraint_rule)\n",
      "        \n",
      "        # Create constraints for the UnsatDemand variables \n",
      "        def unsat_constraint_rule(model, n):\n",
      "            imbalance = self.node_data['SupplyDemand'].get(n,0)\n",
      "            supply_node = int(imbalance < 0)\n",
      "            demand_node = int(imbalance > 0)\n",
      "            if (supply_node):\n",
      "                return -model.rho[n] <= self.nCmax\n",
      "            if (demand_node):\n",
      "                return model.rho[n] <= self.nCmax\n",
      "            return pe.Constraint.Skip\n",
      "\n",
      "        model.UnsatConstraint = pe.Constraint(model.node_set, rule=unsat_constraint_rule)\n",
      "     \n",
      "        # Create the interdiction budget constraint \n",
      "        def block_limit_rule(model):\n",
      "            model.attacks = self.attacks\n",
      "            return pe.summation(model.x) <= model.attacks\n",
      "\n",
      "        model.BlockLimit = pe.Constraint(rule=block_limit_rule)\n",
      "\n",
      "        # Create, save the model\n",
      "        self.Idual = model\n",
      "\n",
      "    def solve(self, tee=False):\n",
      "        solver = pyomo.opt.SolverFactory('cplex')\n",
      "\n",
      "        # Solve the dual first\n",
      "        self.Idual.BlockLimit.construct()\n",
      "        self.Idual.BlockLimit._constructed = False\n",
      "        del self.Idual.BlockLimit._data[None] \n",
      "        self.Idual.BlockLimit.reconstruct()\n",
      "        self.Idual.preprocess()\n",
      "        results = solver.solve(self.Idual, tee=tee, keepfiles=False, options_string=\"mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0\")\n",
      "\n",
      "        # Check that we actually computed an optimal solution, load results\n",
      "        if (results.solver.status != pyomo.opt.SolverStatus.ok):\n",
      "            logging.warning('Check solver not ok?')\n",
      "        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):  \n",
      "            logging.warning('Check solver optimality?')\n",
      "\n",
      "        self.Idual.solutions.load_from(results)\n",
      "        # Now put interdictions into xbar and solve primal\n",
      "       \n",
      "        for e in self.arc_data.index:\n",
      "            self.arc_data.ix[e,'xbar'] = self.Idual.x[e].value\n",
      "\n",
      "        self.primal.OBJ.construct()\n",
      "        self.primal.OBJ._constructed = False\n",
      "        self.primal.OBJ._init_sense = pe.minimize\n",
      "        del self.primal.OBJ._data[None] \n",
      "        self.primal.OBJ.reconstruct()\n",
      "        self.primal.preprocess()\n",
      "        results = solver.solve(self.primal, tee=tee, keepfiles=False, options_string=\"mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0\")\n",
      "\n",
      "        # Check that we actually computed an optimal solution, load results\n",
      "        if (results.solver.status != pyomo.opt.SolverStatus.ok):\n",
      "            logging.warning('Check solver not ok?')\n",
      "        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):  \n",
      "            logging.warning('Check solver optimality?')\n",
      "\n",
      "        self.primal.solutions.load_from(results)\n",
      "\n",
      "    def printSolution(self):\n",
      "        print\n",
      "        print 'Using %d attacks:'%self.attacks\n",
      "        print\n",
      "        edges = sorted(self.arc_set)\n",
      "        for e in edges:\n",
      "            if self.Idual.x[e].value > 0:\n",
      "                print 'Interdict arc %s -> %s'%(str(e[0]), str(e[1]))\n",
      "        print\n",
      "        \n",
      "        nodes = sorted(self.node_data.index)\n",
      "        for n in nodes:\n",
      "            remaining_supply = self.primal.UnsatSupply[n].value\n",
      "            if remaining_supply > 0:\n",
      "                print 'Remaining supply on node %s: %.2f'%(str(n), remaining_supply)\n",
      "        for n in nodes:\n",
      "            remaining_demand = self.primal.UnsatDemand[n].value\n",
      "            if remaining_demand > 0:\n",
      "                print 'Remaining demand on node %s: %.2f'%(str(n), remaining_demand)\n",
      "        print\n",
      "        \n",
      "        for e0,e1 in self.arc_set:\n",
      "            flow = self.primal.y[(e0,e1)].value\n",
      "            if flow > 0:\n",
      "                print 'Flow on arc %s -> %s: %.2f'%(str(e0), str(e1), flow)\n",
      "        print\n",
      "\n",
      "        print '----------'\n",
      "        print 'Total cost = %.2f (primal) %.2f (dual)'%(self.primal.OBJ(), self.Idual.OBJ())\n",
      "\n",
      "\n",
      "########################\n",
      "# Now lets do something\n",
      "########################\n",
      "\n",
      "if __name__ == '__main__':\n",
      "    m = MinCostFlowInterdiction('sample_nodes_data.csv', 'sample_arcs_data.csv')\n",
      "    m.solve()\n",
      "    m.printSolution()\n",
      "    m.attacks = 1\n",
      "    m.solve()\n",
      "    m.printSolution()\n",
      "    m.attacks = 2\n",
      "    m.solve()\n",
      "    m.printSolution()\n"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "\n",
        "Using 0 attacks:\n",
        "\n",
        "\n",
        "\n",
        "Flow on arc B -> End: 30.00\n",
        "Flow on arc C -> B: 20.00\n",
        "Flow on arc Start -> B: 10.00\n",
        "Flow on arc Start -> C: 10.00\n",
        "\n",
        "----------\n",
        "Total cost = 700.00 (primal) 700.00 (dual)\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "\n",
        "Using 1 attacks:\n",
        "\n",
        "Interdict arc Start -> C\n",
        "\n",
        "Remaining supply on node Start: 10.00\n",
        "Remaining demand on node End: 10.00\n",
        "\n",
        "Flow on arc B -> End: 20.00\n",
        "Flow on arc C -> B: 10.00\n",
        "Flow on arc Start -> B: 10.00\n",
        "\n",
        "----------\n",
        "Total cost = 7300.00 (primal) 7300.00 (dual)\n"
       ]
      },
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "\n",
        "Using 2 attacks:\n",
        "\n",
        "Interdict arc B -> End\n",
        "Interdict arc C -> D\n",
        "\n",
        "Remaining supply on node C: 10.00\n",
        "Remaining supply on node Start: 20.00\n",
        "Remaining demand on node End: 30.00\n",
        "\n",
        "\n",
        "----------\n",
        "Total cost = 21000.00 (primal) 21000.00 (dual)\n"
       ]
      }
     ],
     "prompt_number": 2
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [],
     "language": "python",
     "metadata": {},
     "outputs": []
    }
   ],
   "metadata": {}
  }
 ]
}
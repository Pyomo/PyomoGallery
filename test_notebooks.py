#
# Jupyter notebook testing logic adapted from
#   https://gist.github.com/lheagy/f216db7220713329eb3fc1c2cd3c7826
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Lindsey Heagy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Raw


import unittest
import sys
import os
import subprocess
try:
    import jupyter
    jupyter_available = True
except:
    jupyter_available = False
try:
    import pandas
    pandas_available = True
except:
    pandas_available = False
try:
    import networkx
    networkx_available = True
except:
    networkx_available = False

timeout=120

requires_pandas = set(['max_flow_interdict', 'min_cost_flow_interdict', 'multi_commodity_flow_interdict', 'sp_interdict', 'min_cost_flow', 'mst'])
requires_networkx = set(['mst'])


# Testing for the notebooks - use nbconvert to execute all cells of the
# notebook

# For testing on TravisCI, be sure to include a requirements.txt that 
# includes jupyter so that you run on the most up-to-date version. 


# Where are the notebooks?
TESTDIR = os.path.dirname(os.path.abspath(__file__))
#NBDIR = os.path.sep.join(TESTDIR.split(os.path.sep)[:-2] + ['notebooks/']) # where are the notebooks?

def setUp():
    nbpaths = []  # list of notebooks, with file paths
    nbnames = []  # list of notebook names (for making the tests)

    print(TESTDIR)
    # walk the test directory and find all notebooks
    for dirname, dirnames, filenames in os.walk(TESTDIR):
        for filename in filenames:
            if filename.endswith('.ipynb') and not filename.endswith('-checkpoint.ipynb'):
                nbpaths.append(os.path.abspath(dirname) + os.path.sep + filename) # get abspath of notebook
                nbnames.append(''.join(filename[:-6])) # strip off the file extension
    return nbpaths, nbnames


def get(nbname, nbpath):

    # use nbconvert to execute the notebook
    def test_func(self):
        print('\n--------------- Testing {0} ---------------'.format(nbname))
        print('   {0}'.format(nbpath))
        if not jupyter_available:
            self.skipTest("Jupyter unavailable")
        if nbname in requires_pandas and not pandas_available:
            self.skipTest("Pandas unavailable")
        if nbname in requires_networkx and not networkx_available:
            self.skipTest("Networkx unavailable")

        # execute the notebook using nbconvert to generate html 
        dir_=os.path.dirname(nbpath)
        os.chdir(dir_)
        nbexe = subprocess.Popen(
            [ 'jupyter', 'nbconvert', '{0}'.format(nbpath),
              '--execute',
              '--inplace',
              '--ExecutePreprocessor.kernel_name=python%s' % (
                  {2:"",3:"3"}[sys.version_info[0]], ),
              '--ExecutePreprocessor.timeout='+str(timeout)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, err = nbexe.communicate()
        check = nbexe.returncode
        if check == 0:
            print('\n ..... {0} Passed ..... \n'.format(nbname))
            # if passed remove the generated html file
            #subprocess.call(['rm', '{0}.html'.format( os.path.sep.join(os.getcwd().split(os.path.sep) + [nbpath.split(os.path.sep)[-1][:-6]]))])
        else:
            print('\n <<<<< {0} FAILED >>>>> \n'.format(nbname))
            print('Captured Output: \n {0}'.format(err))

        self.assertEqual(check, 0)

    return test_func


class TestNotebooks(unittest.TestCase):
    pass

nbpaths, nbnames = setUp()
# Check for duplicates
tmp = set()
for name in nbnames:
    if name in tmp:
        raise IOError("ERROR: duplicate test name %s" % name)
    tmp.add(name)

# build test for each notebook
for i, nb in enumerate(nbnames):
    #print((i,nb,nbpaths[i]))
    setattr(TestNotebooks, 'test_'+nb, get(nb, nbpaths[i]))


if __name__ == '__main__':
    unittest.main()


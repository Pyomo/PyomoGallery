import pyomo.environ
from pyomo.core import ComponentUID
from pyomo.opt import ProblemFormat
# use fast version of pickle (python 2 or 3)
from six.moves import cPickle as pickle

def write_nl(model, nl_filename, **kwds):
    """
    Writes a Pyomo model in NL file format and stores
    information about the symbol map that allows it to be
    recovered at a later time for a Pyomo model with
    matching component names.
    """
    symbol_map_filename = nl_filename+".symbol_map.pickle"

    # write the model and obtain the symbol_map
    _, smap_id = model.write(nl_filename,
                             format=ProblemFormat.nl,
                             io_options=kwds)
    symbol_map = model.solutions.symbol_map[smap_id]

    # save a persistent form of the symbol_map (using pickle) by
    # storing the NL file label with a ComponentUID, which is
    # an efficient lookup code for model components (created
    # by John Siirola)
    tmp_buffer = {} # this makes the process faster
    symbol_cuid_pairs = tuple(
        (symbol, ComponentUID(var_weakref(), cuid_buffer=tmp_buffer))
        for symbol, var_weakref in symbol_map.bySymbol.items())
    with open(symbol_map_filename, "wb") as f:
        pickle.dump(symbol_cuid_pairs, f)

    return symbol_map_filename

if __name__ == "__main__":
    from script import create_model

    model = create_model()
    nl_filename = "example.nl"
    symbol_map_filename = write_nl(model, nl_filename)
    print("        NL File: %s" % (nl_filename))
    print("Symbol Map File: %s" % (symbol_map_filename))

# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from pyomo.environ import *

from ..constants import *

from pprint import pprint

def index_identify(index):
    return '{{' + index + '}}'

var_order = [ z, z_cu, z_hu, area_beta, area_cu_beta, area_hu_beta, area, area_cu, area_hu, dt, dt_cu, dt_hu, fh, fc, reclmtd, reclmtd_cu, reclmtd_hu, q, q_cu, q_hu, th, tc, thx, tcx, bh_in, bh_out, bc_in, bc_out]

ignored_vars = [z_q, z_q_cu, z_q_hu, var_delta_reclmtd, var_delta_reclmtd_cu, var_delta_reclmtd_hu, z_th, z_thx, z_tc, z_tcx, var_delta_fh, var_delta_fhx, var_delta_fc, var_delta_fcx, z_area_beta, z_area_cu_beta, z_area_hu_beta]

ijk_subscript = '%s,%s,%s' % (index_identify(index_i), index_identify(index_j), index_identify(index_k))
ijk_indices = [ index_i, index_j, index_k ]

cui_subscript = 'cu,%s' % index_identify(index_i)
cui_indices   = [ index_i ]

huj_subscript = 'hu,%s' % index_identify(index_j)
huj_indices   = [ index_j ]

ikSubscript = '%s,%s' % (index_identify(index_i), index_identify(index_k))
ikIndices   = [ index_i, index_k ]

jkSubscript = '%s,%s' % (index_identify(index_j), index_identify(index_k))
jkIndices   = [ index_j, index_k ]

var_to_subscript_map = {\
    area:{\
            latex_label: 'A',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices : ijk_indices\
         },\
    area_cu:{\
            latex_label: 'A',\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    area_hu:{\
            latex_label: 'A',\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            },\
    area_beta:{\
            latex_label: 'A',\
            latex_superscript: r'\beta',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices : ijk_indices\
         },\
    area_cu_beta:{\
            latex_label: 'A',\
            latex_superscript: r'\beta',\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    area_hu_beta:{\
            latex_label: 'A',\
            latex_superscript: r'\beta',\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            },\
    bc_in:{\
            latex_label: 'b',\
            latex_superscript: 'C,\\text{in}',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    bc_out:{\
            latex_label: 'b',\
            latex_superscript: 'C,\\text{out}',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    bh_in:{\
            latex_label: 'b',\
            latex_superscript: 'H,\\text{in}',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    bh_out:{\
            latex_label: 'b',\
            latex_superscript: 'H,\\text{out}',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    dt:{\
            latex_label: 'dt',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    dt_cu:{\
            latex_label: 'dt',\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    dt_hu:{\
            latex_label: 'dt',\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            },\
    fc:{\
            latex_label: 'f',\
            latex_superscript: 'C',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    fh:{\
            latex_label: 'f',\
            latex_superscript: 'H',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    reclmtd:{\
            latex_label: '\\textsl{RecLMTD}',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    reclmtd_cu:{\
            latex_label: '\\textsl{RecLMTD}',\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    reclmtd_hu:{\
            latex_label: '\\textsl{RecLMTD}',\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            },\
    q:{\
            latex_label: 'q',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    q_cu:{\
            latex_label: 'q',\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    q_hu:{\
            latex_label: 'q',\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            },\
    tc:{\
            latex_label: 't',\
            latex_superscript: '(C)',\
            latex_subscript: jkSubscript,\
            subscript_indices: jkIndices,\
            all_indices: jkIndices\
         },\
    th:{\
            latex_label: 't',\
            latex_superscript: '(H)',\
            latex_subscript: ikSubscript,\
            subscript_indices: ikIndices,\
            all_indices: ikIndices\
         },\
    tcx:{\
            latex_label: 't',\
            latex_superscript: 'C',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    thx:{\
            latex_label: 't',\
            latex_superscript: 'H',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    z:{\
            latex_label: 'z',\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    z_cu:{\
            latex_label: 'z',\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    z_hu:{\
            latex_label: 'z',\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            }
}

def order_key(var):
    if var.pyomo_label not in var_to_subscript_map:
        return (float('inf'),)
    return (var_order.index(var.pyomo_label), ) + tuple(var.var_details.get(all_indices))
    

class HeatVar:
    def __init__(self, pyomo_label, index, value):
        self.value = value
        self.subscripts = []
        self.pyomo_label = pyomo_label
        self.index = index if not type(index) == int else (index,)
        self.init_latex_data()

    def init_latex_data(self):
        if self.pyomo_label in var_to_subscript_map:
            self.var_details = var_to_subscript_map.get(self.pyomo_label)
            self.index_map   = dict(zip(self.var_details.get(all_indices), self.index))
        else:
            self.var_details = {}
            self.var_details[latex_label] = '(*)' + self.pyomo_label + '-'+ str(self.index)

    def __getitem__(self, item):
        return getattr(self, item)

    def to_latex(self):
        latex_string = self.var_details[latex_label]
        latex_string += self.buildLatexSubscript()
        latex_string += self.buildLatexSuperscript()
        return latex_string

    def buildLatexSubscript(self):
        subscript = self.substitute_indices_into_template(latex_subscript, subscript_indices)
        return '_{' + subscript + '}' if not subscript == '' else ''

    def buildLatexSuperscript(self):
        superscript = self.substitute_indices_into_template(latex_superscript, superscript_indices)
        return '^{' + superscript + '}' if not superscript == '' else ''

    def substitute_indices_into_template(self, template_key, indices_key):
        template = self.var_details.get( template_key, '')
        indices  = self.var_details.get( indices_key, [] )
        for index in indices:
            template = template.replace(index_identify(index), str(self.index_map.get(index)))
        return template

    def table_row(self):
        return ('$' + self.to_latex() + '$', self.value)

def keep_variable(variable, active_hx):
    if variable.pyomo_label in [z, area, q, reclmtd, area_beta, fh, fc, bh_in, bh_out, bc_in, bc_out, thx, tcx]:
        return variable.index in active_hx[stream_hx]
    elif variable.pyomo_label in [z_cu, area_cu, q_cu, reclmtd_cu, area_cu_beta, dt_cu]:
        return variable.index[0] in active_hx[cu_hx]
    elif variable.pyomo_label in [z_hu, area_hu, q_hu, reclmtd_hu, area_hu_beta, dt_hu]:
        return variable.index[0] in active_hx[hu_hx]
    elif variable.pyomo_label in [dt]:
        index  = variable.index
        index2 = (index[0], index[1], index[2]-1)
        return index in active_hx[stream_hx] or index2 in active_hx[stream_hx]
    return True

def parse_pyomo_results(instance, active_hx):
    results = []
    for var in instance.component_objects(Var):
        var_str = var.name
        if var_str not in ignored_vars:
            for k, v in var.iteritems():
                results.append(HeatVar(var_str, k, v.value))

    active_variables = sorted([v for v in results if keep_variable(v, active_hx)], key=order_key)
    inactive_variables = sorted([v for v in results if not keep_variable(v, active_hx)], key=order_key)

    return (active_variables, inactive_variables)

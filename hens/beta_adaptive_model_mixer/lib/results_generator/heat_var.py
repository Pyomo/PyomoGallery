# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from pyomo.environ import *


from ..constants import *

def index_identify(index):
    return '{{' + index + '}}'

var_order = [ z, z_cu, z_hu, area_beta, area_cu_beta, area_hu_beta, area, area_cu, area_hu, dt, dt_cu, dt_hu, fh, fc, reclmtd, reclmtd_CU, reclmtd_HU, reclmtd_beta, reclmtd_cu_beta, reclmtd_hu_beta, q, q_cu, q_hu, q_beta, q_cu_beta, q_hu_beta, th, tc, thx, tcx, bh_in, bh_out, bc_in, bc_out]

ignored_vars = [z_A, z_A_CU, z_A_HU, z_q, z_q_CU, z_q_HU, z_th, z_thx, z_tc, z_tcx, var_delta_fh, var_delta_fhx, var_delta_fc, var_delta_fcx, z_A_beta, z_A_CU_beta, z_A_HU_beta, z_q_beta, z_q_cu_beta, z_q_hu_beta, var_delta_reclmtd_beta, var_delta_reclmtd_cu_beta, var_delta_reclmtd_hu_beta, z_area_beta_q, z_area_beta_q_cu, z_area_beta_q_hu]

ijk_subscript = '%s,%s,%s' % (index_identify(index_i), index_identify(index_j), index_identify(index_k))
ijk_indices = [ index_i, index_j, index_k ]

cui_subscript = 'cu,%s' % index_identify(index_i)
cui_indices   = [ index_i ]

huj_subscript = 'hu,%s' % index_identify(index_j)
huj_indices   = [ index_j ]

ik_subscript = '%s,%s' % (index_identify(index_i), index_identify(index_k))
ik_indices   = [ index_i, index_k ]

jk_subscript = '%s,%s' % (index_identify(index_j), index_identify(index_k))
jk_indices   = [ index_j, index_k ]

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
            latex_superscript: ltx_beta,\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices : ijk_indices\
         },\
    area_cu_beta:{\
            latex_label: 'A',\
            latex_superscript: ltx_beta,\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    area_hu_beta:{\
            latex_label: 'A',\
            latex_superscript: ltx_beta,\
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
    reclmtd_beta:{\
            latex_label: '\\textsl{RecLMTD}',\
            latex_superscript: ltx_beta,\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    reclmtd_cu_beta:{\
            latex_label: '\\textsl{RecLMTD}',\
            latex_superscript: ltx_beta,\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    reclmtd_hu_beta:{\
            latex_label: '\\textsl{RecLMTD}',\
            latex_superscript: ltx_beta,\
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
    q_beta:{\
            latex_label: 'q',\
            latex_superscript: ltx_beta,\
            latex_subscript: ijk_subscript,\
            subscript_indices: ijk_indices,\
            all_indices: ijk_indices\
         },\
    q_cu_beta:{\
            latex_label: 'q',\
            latex_superscript: ltx_beta,\
            latex_subscript: cui_subscript,\
            subscript_indices: cui_indices,\
            all_indices: cui_indices\
            },\
    q_hu_beta:{\
            latex_label: 'q',\
            latex_superscript: ltx_beta,\
            latex_subscript: huj_subscript,\
            subscript_indices: huj_indices,\
            all_indices: huj_indices\
            },\
    tc:{\
            latex_label: 't',\
            latex_superscript: '(C)',\
            latex_subscript: jk_subscript,\
            subscript_indices: jk_indices,\
            all_indices: jk_indices\
         },\
    th:{\
            latex_label: 't',\
            latex_superscript: '(H)',\
            latex_subscript: ik_subscript,\
            subscript_indices: ik_indices,\
            all_indices: ik_indices\
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

def list_to_delimited_string(values, delimiter):
    return str(delimiter).join(map(str, values))

def filter_dict(dictionary, keys):
    return { k:v for k,v in dictionary.iteritems() if k in keys }

# def order_var(var1, var2):
#     if var1.pyomo_label not in var_to_subscript_map:
#         return 1
#     if var2.pyomo_label not in var_to_subscript_map:
#         return -1
#     var1_label_order = var_order.index(var1.pyomo_label)
#     var2_label_order = var_order.index(var2.pyomo_label)
#     if var1_label_order < var2_label_order :
#         return -1
#     elif var1_label_order > var2_label_order:
#         return 1
#     else:
#         indices = var1.var_details.get(all_indices)
#         for index in indices:
#             if var1.index_map.get(index) < var2.index_map.get(index):
#                 return -1
#             elif var1.index_map.get(index) > var2.index_map.get(index):
#                 return 1
#         return 0

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
        latex_string += self.build_latex_subscript()
        latex_string += self.build_latex_superscript()
        return latex_string

    def build_latex_subscript(self):
        subscript = self.substitute_indices_into_template(latex_subscript, subscript_indices)
        return '_{' + subscript + '}' if not subscript == '' else ''

    def build_latex_superscript(self):
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
    if variable.pyomo_label in stream_keep_variables:
        return variable.index in active_hx[stream_hx]
    elif variable.pyomo_label in cu_keep_variables:
        return variable.index[0] in active_hx[cu_hx]
    elif variable.pyomo_label in hu_keep_variables:
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

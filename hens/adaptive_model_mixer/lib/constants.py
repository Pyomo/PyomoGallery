# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

stream_hx = 'stream_hx'
cu_hx = 'cu_hx'
hu_hx = 'hu_hx'

bal_eps  = 'bal_eps'
lmtd_eps = 'lmtd_eps'
area_eps = 'area_eps'
beta_eps = 'beta_eps'

balancing_ref = 'balancing_ref'
reclmtd_ref   = 'reclmtd_ref'
area_ref      = 'area_ref'
beta_ref      = 'beta_ref'

breakpoints = 'breakpoints'

lbl_model = 'model'

model1 = lbl_model + '1'
model2 = lbl_model + '2'
model3 = lbl_model + '3'

active_lb = 0.9

default_stream_tangent_weights = \
    [\
        (1,0,0),\
        (0,1,0),\
        (0,0,1),\
        (0.5,0.5,0),\
        # (0.75,0.25,0),\
        # (0.25,0.75, 0),\
        # (1/3, 1/3, 1/3),\
        # (1/2, 1/4, 1/4),\
        # (1/4, 1/2, 1/4),\
        # (1/4, 1/4, 1/2)\
    ]

default_utility_tangent_weights = \
    [\
        (1,0),\
        (0,1),\
        # (0.75,0.25),\
        (0.5,0.5),\
        # (0.25,0.75)\
    ]

defaultTangentWeights = \
    {\
        stream_hx:  default_stream_tangent_weights,\
        cu_hx:      default_utility_tangent_weights,\
        hu_hx:      default_utility_tangent_weights\
    }

iterations = 'iterations'
logs       = 'logs'

model_folder      = 'model_folder'
append_folder     = 'append_folder'
iterations_folder = 'iterations_folder'
logs_folder       = 'logs_folder'

absolute_error = 'absolute_error'
relative_error = 'relative_error'

reclmtd_error   = 'reclmtd_error'
area_error      = 'area_error'
area_beta_error = 'area_beta_error'
bhin_error      = 'bhin_error'
bhout_error     = 'bhout_error'
bcin_error      = 'bcin_error'
bcout_error     = 'bcout_error'

tangent_points   = 'tangent_points'
q_points         = 'q_points'
area_beta_points = 'area_beta_points'
th_points        = 'th_points'
thx_points       = 'thx_points'
tc_points        = 'tc_points'
tcx_points       = 'tcx_points'

index_i = 'i'
index_j = 'j'
index_k = 'k'

index_m = 'm'
index_n = 'n'

#Dictionary Keys
latex_label         = 'latex_label'
latex_subscript     = 'latex_subscript'
latex_superscript   = 'latex_superscript'
subscript_indices   = 'subscript_indices'
superscript_indices = 'superscript_indices'
all_indices         = 'all_indices'

#Model Labels
area    = 'area'
area_cu = 'area_cu'
area_hu = 'area_hu'

area_beta    = 'area_beta'
area_cu_beta = 'area_cu_beta'
area_hu_beta = 'area_hu_beta'

bh_in  = 'bh_in'
bh_out = 'bh_out'
bc_in  = 'bc_in'
bc_out = 'bc_out'

dt    = 'dt'
dt_cu = 'dt_cu'
dt_hu = 'dt_hu'

fh = 'fh'
fc = 'fc'

reclmtd    = 'reclmtd'
reclmtd_cu = 'reclmtd_cu'
reclmtd_hu = 'reclmtd_hu'

q    = 'q'
q_cu = 'q_cu'
q_hu = 'q_hu'

th = 'th'
tc = 'tc'

thx = 'thx'
tcx = 'tcx'

z    = 'z'
z_cu = 'z_cu'
z_hu = 'z_hu'

z_q    = 'z_q'
z_q_cu = 'z_q_cu'
z_q_hu = 'z_q_hu'

var_delta_reclmtd    = 'var_delta_reclmtd'
var_delta_reclmtd_cu = 'var_delta_reclmtd_cu'
var_delta_reclmtd_hu = 'var_delta_reclmtd_hu'

z_th  = 'z_th'
z_thx = 'z_thx'
z_tc  = 'z_tc'
z_tcx = 'z_tcx'

var_delta_fh  = 'var_delta_fh'
var_delta_fhx = 'var_delta_fhx'
var_delta_fc  = 'var_delta_fc'
var_delta_fcx = 'var_delta_fcx'

z_area_beta    = 'z_area_beta'
z_area_cu_beta = 'z_area_cu_beta'
z_area_hu_beta = 'z_area_hu_beta'

model_map = {\
            'model1': 'http://www.gamsworld.org/minlp/minlplib2/html/heatexch_gen1.html',\
            'model2': 'http://www.gamsworld.org/minlp/minlplib2/html/heatexch_gen2.html',\
            'model3': 'http://www.gamsworld.org/minlp/minlplib2/html/heatexch_gen3.html'\
            }

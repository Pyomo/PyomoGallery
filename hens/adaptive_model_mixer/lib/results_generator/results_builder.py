# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

import json, sys, unicodedata, os, yaml

from pyomo.environ import *

from . import heat_var

from .document_builder import *

from pprint import pprint

from ..constants import *

try:
    from pylatex import *

    def build_heat_exchanger_results_doc(results, folders, append, iter_num, datafile_model, filename, instance, active_hx, old_points, errors, local_time, total_time, epsilons, tolerances, iteration):
        level = 0

        beta = instance.Beta
        tac = value(instance.TAC)

        check_folder_structure(folders, iteration)

        doc = Document()
        add_preamble(doc)

        doc.append(NoEscape(r'\section{Summary}'))
        doc.append(NoEscape(r'\thispagestyle{plain}'))
        add_summary(datafile_model, append, iter_num, tac, local_time, total_time, epsilons, tolerances, doc, level)

        doc.append(NoEscape(r'\clearpage'))

        doc.append(NoEscape(r'\section{Results}'))
        doc.append(NoEscape(r'\thispagestyle{plain}'))
        add_active_results_table(doc, results, level)
        doc.append(NoEscape(r'\clearpage'))

        doc.append(NoEscape(r'\section{$\textsl{RecLMTD}$ Tangent Points}'))
        doc.append(NoEscape(r'\thispagestyle{plain}'))
        add_reclmtd_results(instance, active_hx, errors, doc, level)
        generate_reclmtd_graphs(instance, active_hx, old_points, doc, level)

        doc.append(NoEscape(r'\clearpage'))

        doc.append(NoEscape(r'\section{Balancing Breakpoints}'))
        add_balancing_results(instance, active_hx, old_points, errors, doc, level)
        generate_balancing_graphs(instance, active_hx, old_points, doc, level)

        doc.append(NoEscape(r'\clearpage'))
        doc.append(NoEscape(r'\section{Area Breakpoints}'))
        doc.append(NoEscape(r'\thispagestyle{plain}'))
        add_area_results(instance, active_hx, old_points, errors, doc, level)
        add_area_graphs(instance, active_hx, old_points, doc, level)

        doc.append(NoEscape(r'\clearpage'))
        doc.append(NoEscape(r'\section{$A^\beta$ Breakpoints}'))
        doc.append(NoEscape(r'\thispagestyle{plain}'))
        add_area_beta_results(instance, active_hx, old_points, errors, doc, level)
        add_area_beta_graphs(instance, active_hx, old_points, doc, level)

        doc.append(NoEscape(r'\clearpage'))
        doc.append(NoEscape(r'\section{Other variables}'))
        doc.append(NoEscape(r'\thispagestyle{plain}'))
        add_inactive_results_table(results, doc, level)

        save_pdf(doc, filename, folders, iteration)
except ImportError:
    def build_heat_exchanger_results_doc(results, folders, append, iter_num, datafile_model, filename, instance, active_hx, old_points, errors, local_time, total_time, epsilons, tolerances, iteration):
        check_folder_structure(folders, iteration)
        with open(os.path.join(folders[iterations_folder], filename + '.txt'), 'w') as f:
            f.write('You don\'t have pylatex. Install it with pip for results summary.\n')

def build_heat_exchanger_results(instance, folders, append, iter_num,  datafile_model, filename, active_hx, old_points, errors, local_time, total_time, epsilons, tolerances, iteration=False):
    results = heat_var.parse_pyomo_results(instance, active_hx)
    build_heat_exchanger_results_doc(results, folders, append, iter_num, datafile_model, filename, instance, active_hx, old_points, errors, local_time, total_time, epsilons, tolerances, iteration)

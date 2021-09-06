# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

import json, sys, unicodedata, os, yaml

from pyomo.environ import *
from pprint import pprint

from ..constants import *


try:
    from pylatex import *
except ImportError:
    pass

def check_folder_structure(folders, iteration):
    if not os.path.exists(folders[model_folder]):
        os.makedirs(folders[model_folder])

    if not os.path.exists(folders[append_folder]):
        os.makedirs(folders[append_folder])

    if iteration and not os.path.exists(folders[iterations_folder]):
        os.makedirs(folders[iterations_folder])

def save_pdf(doc, filename, folders, iteration):
    if iteration:
        path_without_extension = os.path.join(folders[iterations_folder], filename)
    else:
        path_without_extension = os.path.join(folders[append_folder], filename)

    doc.generate_pdf(path_without_extension, silent=True)
    if (len(sys.argv) > 2):
        with open(path_without_extension + '.tex', 'w') as tex_file:
            tex_file.write(doc.dumps())

def add_preamble(doc):
    doc.packages.append(Package('float, amsmath, amssymb, supertabular, multicol, url, subcaption, tikz, pgfplots, fancyhdr, morefloats, setspace'))
    doc.packages.append(Package('parskip', options=['parfill']))
    doc.packages.append(Package('geometry', options=['tmargin=1in', 'lmargin=0.5in', 'rmargin=1in', 'bmargin=20mm']))

    doc.preamble.append(NoEscape(r'\usetikzlibrary{calc}'))

    # doc.preamble.append('\pgfplotsset{compat=1.10}')
    doc.preamble.append(NoEscape(r'\pgfplotsset{samples=500}'))
    # doc.preamble.append('\usepgfplotslibrary{fillbetween}')

    doc.preamble.append(NoEscape(r'\renewcommand{\arraystretch}{1.5}'))
    doc.preamble.append(NoEscape(r'\setlength{\columnseprule}{0.4pt}'))

    doc.preamble.append(NoEscape(r'\makeatletter'))
    doc.preamble.append(NoEscape(r'\let\mcnewpage=\newpage'))
    doc.preamble.append(NoEscape(r'\newcommand{\TrickSupertabularIntoMulticols}{%'))
    doc.preamble.append(NoEscape(r'\renewcommand\newpage{%'))
    doc.preamble.append(NoEscape(r'\if@firstcolumn'))
    doc.preamble.append(NoEscape(r'\hrule width\linewidth height0pt'))
    doc.preamble.append(NoEscape(r'\columnbreak'))
    doc.preamble.append(NoEscape(r'\else'))
    doc.preamble.append(NoEscape(r'\mcnewpage'))
    doc.preamble.append(NoEscape(r'\fi'))
    doc.preamble.append(NoEscape(r'}%'))
    doc.preamble.append(NoEscape(r'}'))
    doc.preamble.append(NoEscape(r'\makeatother'))
    doc.preamble.append(NoEscape(r'\relax'))
    doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
    doc.preamble.append(NoEscape(r'\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}'))

def add_summary(datafile_model, append, iter_num, tac, local_time, total_time, epsilons, tolerances, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{spacing}{1.3}' % (tab_gap)))
    level = level + 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\Large' % (tab_gap)))
    doc.append(NoEscape(r'%sModel (Run-name): %s (%s)\\' % (tab_gap, datafile_model, append)))
    # doc.append('Run name: %s\\\\' % append)
    doc.append(NoEscape(r'%sIteration: %d\\' % (tab_gap, iter_num)))
    doc.append(NoEscape(r'%s\textbf{TAC: %s}\\' % (tab_gap, str(tac))))
    doc.append(NoEscape(r'%sTook: %ss\\' % (tab_gap, str(local_time))))
    doc.append(NoEscape(r'%sTotal Time: %ss\\' % (tab_gap, str(total_time))))
    doc.append(NoEscape(r'%sEpsilons:' % (tab_gap)))
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level = level + 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\item $\varepsilon_{\textsl{Balancing}}$: %s' % (tab_gap,  str(epsilons[balancing_ref]))))
    doc.append(NoEscape(r'%s\item $\varepsilon_{\textsl{q-$\beta$}}$: %s' % (tab_gap, str(epsilons[q_beta_ref]))))
    doc.append(NoEscape(r'%s\item $\varepsilon_{\textsl{RecLMTD-$\beta$}}$: %s' % (tab_gap, str(epsilons[lmtd_beta_ref]))))
    doc.append(NoEscape(r'%s\item $\varepsilon_{\textsl{Area-$\beta$}}$: %s' % (tab_gap, str(epsilons[area_beta_ref]))))
    level = level - 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))
    doc.append(NoEscape(r'%sGurobi Tolerances:' % (tab_gap)))
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level = level + 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\item IntFeasTol: %s' % (tab_gap,  str(tolerances['IntFeasTol']))))
    doc.append(NoEscape(r'%s\item FeasibilityTol: %s' % (tab_gap, str(tolerances['FeasibilityTol']))))
    doc.append(NoEscape(r'%s\item OptimalityTol: %s' % (tab_gap, str(tolerances['OptimalityTol']))))
    level = level - 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))
    level = level - 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{spacing}' % (tab_gap)))
    # doc.append('\\linespread{1}')
    doc.append(NoEscape(r'%s\normalsize' % (tab_gap)))

    if datafile_model in model_map:
        doc.append(NoEscape(r'%sGamsworld Solution: \url{%s}' % (tab_gap, model_map[datafile_model])))

    doc.append('')
    doc.append(NoEscape(r'%% hello'))

def add_active_results_table(doc, results, level):
    tab_gap = '\t'*level

    doc.append(NoEscape(r'%s\begin{multicols*}{3}' % (tab_gap)))
    doc.append(NoEscape(r'%s\TrickSupertabularIntoMulticols' % (tab_gap)))
    doc.append(NoEscape(r'%s\tablehead{Variable&Value\\\hline}' % (tab_gap)))
    doc.append(NoEscape(r'%s\begin{supertabular}{lr}' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    for result in results[0]:
        result_row = result.table_row()
        doc.append(NoEscape(r'%s%s & %s \\' % (tab_gap, result_row[0], result_row[1])))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{supertabular}' % (tab_gap)))
    doc.append(NoEscape(r'%s\end{multicols*}' % (tab_gap)))

def generate_balancing_list(value, abs_error, rel_error, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\item Value: %s' % (tab_gap, str(value))))
    doc.append(NoEscape(r'%s\item Absolute error: %s' % (tab_gap, str(abs_error))))
    doc.append(NoEscape(r'%s\item Relative error: %s' % (tab_gap, str(rel_error))))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_balancing_results(instance, active_hx, old_points, errors, doc, level):
    tab_gap = '\t'*level
    for group in [bhin_error, bhout_error, bcin_error, bcout_error]:
        if group == bhin_error:
            section_header = r'$b^{\textsl{H},\text{in}}$'
            var = instance.bh_in
        elif group == bhout_error:
            section_header = r'$b^{\textsl{H},\text{out}}$'
            var = instance.bh_out
        elif group == bcin_error:
            section_header = r'$b^{\textsl{C},\text{in}}$'
            var = instance.bc_in
        elif group == bcout_error:
            section_header = r'$b^{\textsl{C},\text{out}}$'
            var = instance.bc_out
        doc.append(NoEscape(r'%s\subsection{%s}' % (tab_gap, section_header)))
        doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
        level = level + 1
        tab_gap = '\t'*level
        for active in active_hx[stream_hx]:
            val = var[active].value
            abs_error = errors[stream_hx][group][active][absolute_error]
            rel_error = errors[stream_hx][group][active][relative_error]

            doc.append(NoEscape(r'%s\item $%s$' % (tab_gap, str(active))))
            generate_balancing_list(val, abs_error, rel_error, doc, level)

        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_num_line_tikz_preamble(x_min, x_max, y_min, y_max, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s[' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%shide axis,' % (tab_gap)))
    doc.append(NoEscape(r'%saxis equal image,' % (tab_gap)))
    doc.append(NoEscape(r'%sscale only axis,' % (tab_gap)))
    doc.append(NoEscape(r'%swidth=\textwidth,' % (tab_gap)))
    doc.append(NoEscape(r'%sxmin=%.15f, xmax=%.15f,' % (tab_gap, x_min, x_max)))
    doc.append(NoEscape(r'%symin=%.15f, ymax=%.15f,' % (tab_gap, y_min, y_max)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s]' % (tab_gap)))

def generate_balancing_graphs(instance, active_hx, old_points, doc, level):
    tab_gap = '\t'*level

    for group in [th_points, thx_points, tc_points, tcx_points]:
        if group == th_points:
            index_extractor = lambda i,j,k: (i,k)
            temp_str = 'H'
            var = instance.th
        elif group == thx_points:
            index_extractor = lambda i,j,k: (i,j,k)
            temp_str = 'H'
            var = instance.thx
        elif group == tc_points:
            index_extractor = lambda i,j,k: (j,k+1)
            temp_str = 'C'
            var = instance.tc
        elif group == tcx_points:
            index_extractor = lambda i,j,k: (i,j,k)
            temp_str = 'C'
            var = instance.tcx
        for active in active_hx[stream_hx]:
            break_index = index_extractor(*active)
            caption = r'$\textit{t}^{\textsl{(%s)}}$ - $%s$' % (temp_str, str(break_index))

            breakpoints = old_points[stream_hx][group][break_index]

            x_min, x_max = var[break_index].bounds
            val = var[break_index].value
            diff = x_max - x_min
            delta = diff/30
            y_min = -(1.5*delta)
            y_max = (-1)*y_min

            doc.append(NoEscape(r'%s\begin{figure}[p]' % (tab_gap)))
            level += 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\centering' % (tab_gap)))

            doc.append(NoEscape(r'%s\begin{subfigure}{\linewidth}' % (tab_gap)))
            level += 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\centering' % (tab_gap)))
            doc.append(NoEscape(r'%s\resizebox{\linewidth}{!}{' % (tab_gap)))
            doc.append(NoEscape(r'%s\begin{tikzpicture}' % (tab_gap)))
            doc.append(NoEscape(r'%s\begin{axis}' % (tab_gap)))
            add_num_line_tikz_preamble(x_min, x_max, y_min, y_max, doc, level)
            level += 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\draw (axis cs: %.15f,0) -- (axis cs: %.15f,0);' % (tab_gap, x_min,x_max)))
            for x in breakpoints:
                lval = (tab_gap, x,delta,x, delta)
                doc.append(NoEscape(r'%s\draw (axis cs: %.15f,-%.15f) -- (axis cs: %.15f,%.15f);' % lval))

            doc.append(NoEscape(r'%s\draw[color=red] (axis cs: %.15f,-%.15f) -- (axis cs: %.15f,%.15f);' % (tab_gap, val,1.5*delta,val,1.5*delta)))

            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{axis}' % (tab_gap)))
            doc.append(NoEscape(r'%s\end{tikzpicture}' % (tab_gap)))
            doc.append(NoEscape(r'%s}' % (tab_gap)))
            doc.append(NoEscape(r'%s\caption{%s}' % (tab_gap, caption)))
            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{subfigure}%s' % (tab_gap, '%')))
            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))

def generate_reclmtd_beta_list(reclmtd_beta_value, abs_error, rel_error, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\item Value: %f' % (tab_gap, reclmtd_beta_value)))
    doc.append(NoEscape(r'%s\item Error: %.15f' % (tab_gap, abs_error)))
    doc.append(NoEscape(r'%s\item Relative error: %.15f' % (tab_gap, rel_error)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_reclmtd_beta_results(instance, active_hx, errors, doc, level):
    doc.append(NoEscape(r'%'*45))
    doc.append(NoEscape(r'%s  $\textsl{RecLMTD}^\beta$ Results  %s' % ('%'*13, '%'*13)))
    doc.append(NoEscape(r'%'*45))

    doc.append(NoEscape(r'\begin{itemize}'))
    level += 1
    tab_gap = '\t'*level
    for active in active_hx[stream_hx]:
        reclmtd_beta_value = value(instance.reclmtd_beta[active])
        abs_error = errors[stream_hx][reclmtd_beta_error][active][absolute_error]
        rel_error = errors[stream_hx][reclmtd_beta_error][active][relative_error]

        doc.append(NoEscape(r'%s\item $%s$' % (tab_gap, str(active))))
        generate_reclmtd_beta_list(reclmtd_beta_value, abs_error, rel_error, doc, level)

    for active in active_hx[cu_hx]:
        reclmtd_beta_value = value(instance.reclmtd_cu_beta[active])
        abs_error = errors[cu_hx][reclmtd_beta_error][active][absolute_error]
        rel_error = errors[cu_hx][reclmtd_beta_error][active][relative_error]

        doc.append(NoEscape(r'%s\item $\textit{cu},%s$' % (tab_gap, str(active))))
        generate_reclmtd_beta_list(reclmtd_beta_value, abs_error, rel_error, doc, level)

    for active in active_hx[hu_hx]:
        reclmtd_beta_value = value(instance.reclmtd_hu_beta[active])
        abs_error = errors[hu_hx][reclmtd_beta_error][active][absolute_error]
        rel_error = errors[hu_hx][reclmtd_beta_error][active][relative_error]

        doc.append(NoEscape(r'%s\item $\textit{hu},%s$' % (tab_gap, str(active))))
        generate_reclmtd_beta_list(reclmtd_beta_value, abs_error, rel_error, doc, level)

    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_reclmtd_beta_tikz_preamble(minn, maxx, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s[' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%saxis lines=middle,' % (tab_gap)))
    doc.append(NoEscape(r'%sxmin=%.15f, xmax=%.15f,' % (tab_gap, minn, maxx)))
    doc.append(NoEscape(r'%symin=%.15f, ymax=%.15f,' % (tab_gap, minn, maxx)))
    doc.append(NoEscape(r'%sxtick=\empty, ytick=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%sxticklabels=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%syticklabels=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%sxlabel=\empty,ylabel=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%severy axis x label/.style={' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%sat={(ticklabel* cs:1)},' % (tab_gap)))
    doc.append(NoEscape(r'%sanchor=west,' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s},' % (tab_gap)))
    doc.append(NoEscape(r'%severy axis y label/.style={' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%sat={(ticklabel* cs:1)},' % (tab_gap)))
    doc.append(NoEscape(r'%sanchor=south,' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s}' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s]' % (tab_gap)))

def generate_reclmtd_beta_graphs(instance, active_hx, old_points, doc, level):
    tab_gap = '\t'*level
    iteration = 0
    for active in active_hx[stream_hx]:
        breakpoints = old_points[stream_hx][tangent_points][active]
        minn, maxx = instance.dt[active].bounds
        xv = value(instance.dt[active])
        yv = value(instance.dt[active[0], active[1], active[2]+1])

        if iteration % 2 == 0:
            doc.append(NoEscape(r'%s\begin{figure}[p]' % (tab_gap)))
            level += 1
            tab_gap = '\t'*level
            if not iteration == 0:
                doc.append(NoEscape(r'%s\ContinuedFloat' % (tab_gap)))
            doc.append(NoEscape(r'%s\centering' % (tab_gap)))
        doc.append(NoEscape(r'%s\begin{subfigure}{0.5\linewidth}' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\centering' % (tab_gap)))
        doc.append(NoEscape(r'%s\begin{tikzpicture}[baseline]' % (tab_gap)))
        doc.append(NoEscape(r'%s\begin{axis}' % (tab_gap)))
        add_reclmtd_beta_tikz_preamble(minn, maxx, doc, level)

        level += 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\draw[dashed] (axis cs: %.15f,%.15f) -- ( axis cs: %.15f,%.15f);' % (tab_gap, minn, minn, maxx, maxx)))
        doc.append('')
        doc.append(NoEscape(r'%s\addplot[only marks] table {' % (tab_gap)))
        for (x,y) in breakpoints:
            doc.append(NoEscape(r'%s%s%.15f %.15f' % (tab_gap, '\t', x,y)))
        doc.append(NoEscape(r'%s};' % (tab_gap)))
        doc.append('')
        doc.append(NoEscape(r'%s\addplot[only marks, mark=+, color=red, thick] table {' % (tab_gap)))
        doc.append(NoEscape(r'%s%s%.15f %.15f' % (tab_gap, '\t', xv, yv)))
        doc.append(NoEscape(r'%s};' % (tab_gap)))
        doc.append('')
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{axis}' % (tab_gap)))
        doc.append(NoEscape(r'%s\end{tikzpicture}' % (tab_gap)))
        doc.append(NoEscape(r'%s\caption{$\textsl{RecLMTD}$ - $%s$}' % (tab_gap, str(active))))
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{subfigure}%s' % (tab_gap, '%%')))
        if iteration % 2 == 1:
            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))
        iteration += 1

    if iteration % 2 == 1:
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))

    iteration = 0
    for active in active_hx[cu_hx]:
        breakpoints = old_points[cu_hx][tangent_points][active]
        minn, maxx = instance.dt_cu[active].bounds
        val = value(instance.dt_cu[active])
        diff = maxx - minn
        delta = diff/30

        doc.append(NoEscape(r'%s\begin{figure}[p]' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        if not iteration == 0:
            doc.append(NoEscape(r'%s\ContinuedFloat' % (tab_gap)))
        doc.append(NoEscape(r'%s\centering' % (tab_gap)))

        doc.append(NoEscape(r'%s\begin{subfigure}{\linewidth}' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\centering' % (tab_gap)))
        doc.append(NoEscape(r'%s\resizebox{0.95\textwidth}{!}{' % (tab_gap)))
        doc.append(NoEscape(r'%s\begin{tikzpicture}[baseline]' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\draw (%.15f,0) -- (%.15f,0);' % (tab_gap,minn,maxx)))
        for x in breakpoints:
            lval = (tab_gap,x,delta,x, delta)
            doc.append(NoEscape(r'%s\draw (%.15f,-%.15f) -- (%.15f,%.15f);' % (lval)))

        doc.append(NoEscape(r'%s\draw[color=red] (%.15f,-%.15f) -- (%.15f,%.15f);' % (tab_gap,val,1.5*delta,val,1.5*delta)))

        level -= 1
        tab_gap = '\t'*level

        doc.append(NoEscape(r'%s\end{tikzpicture}' % (tab_gap)))
        doc.append(NoEscape(r'%s}' % (tab_gap)))
        doc.append(NoEscape(r'%s\caption{$\textsl{RecLMTD}$ - $\textsl{cu},%s$}' % (tab_gap,str(active))))
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{subfigure}%s' % (tab_gap, '%%')))
        # if iteration % 2 == 1:
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))
        iteration += 1

    iteration = 0
    for active in active_hx[hu_hx]:
        breakpoints = old_points[hu_hx][tangent_points][active]
        minn, maxx = instance.dt_hu[active].bounds
        val = value(instance.dt_hu[active])
        diff = maxx - minn
        delta = diff/30


        doc.append(NoEscape(r'%s\begin{figure}[p]' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        if not iteration == 0:
            doc.append(NoEscape(r'%s\ContinuedFloat' % (tab_gap)))
        doc.append(NoEscape(r'%s\centering' % (tab_gap)))

        doc.append(NoEscape(r'%s\begin{subfigure}{\linewidth}' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\centering' % (tab_gap)))
        doc.append(NoEscape(r'%s\resizebox{0.95\linewidth}{!}{' % (tab_gap)))
        doc.append(NoEscape(r'%s\begin{tikzpicture}[baseline]' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\draw (%.15f,0) -- (%.15f,0);' % (tab_gap,minn,maxx)))
        for x in breakpoints:
            lval = (tab_gap,x,delta,x, delta)
            doc.append(NoEscape(r'%s\draw (%.15f,-%.15f) -- (%.15f,%.15f);' % (lval)))

        doc.append(NoEscape(r'%s\draw[color=red] (%.15f,-%.15f) -- (%.15f,%.15f);' % (tab_gap,val,1.5*delta,val,1.5*delta)))
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{tikzpicture}' % (tab_gap)))
        doc.append(NoEscape(r'%s}'% (tab_gap)))
        doc.append(NoEscape(r'%s\caption{$\textsl{RecLMTD}$ - $\textsl{hu},%s$}' % (tab_gap,str(active))))
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{subfigure}%s' % (tab_gap, '%%')))

        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))
        iteration += 1

def generate_q_beta_list(q_value, q_beta, beta, breakpoints, abs_error, rel_error, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level +=1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\item $q$: %f' % (tab_gap, q_value)))
    doc.append(NoEscape(r'%s\item $\hat{q}^\beta$: %f' % (tab_gap, q_beta) ))
    doc.append(NoEscape(r'%s\item $q^\beta$: %f' % (tab_gap, pow(q_value, beta))))
    doc.append(NoEscape(r'%s\item Breakpoints: %s' % (tab_gap, breakpoints)))
    doc.append(NoEscape(r'%s\item Error: %.15f' % (tab_gap, abs_error)))
    doc.append(NoEscape(r'%s\item Relative error: %.15f' % (tab_gap, rel_error)))
    level -=1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_q_beta_results(instance, active_hx, old_points, errors, doc, level):
    beta = instance.Beta

    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level = level + 1
    tab_gap = '\t'*level

    for group in [stream_hx, cu_hx, hu_hx]:
        if group == stream_hx:
            index_template = r'$%s$'
            q_var = instance.q
            q_beta_var = instance.q_beta
        elif group == cu_hx:
            index_template = r'$\textit{cu},%s$'
            q_var = instance.q_cu
            q_beta_var = instance.q_cu_beta
        elif group == hu_hx:
            index_template = r'$\textit{hu},%s$'
            q_var = instance.q_hu
            q_beta_var = instance.q_hu_beta

        for active in active_hx[group]:
            index_str = index_template % (str(active))
            q_value = q_var[active].value
            q_beta = q_beta_var[active].value
            breakpoints = get_breakpoint_list(old_points[group][q_beta_points][active], q_value)
            abs_error = errors[group][q_beta_error][active][absolute_error]
            rel_error = errors[group][q_beta_error][active][relative_error]

            doc.append(NoEscape(r'%s\item %s' % (tab_gap, index_str)))
            generate_q_beta_list(q_value, q_beta, beta, breakpoints, abs_error, rel_error, doc, level)

    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_q_beta_tikz_preamble(x_min, x_max, y_min, y_max, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s[' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%saxis lines=middle,' % (tab_gap)))
    doc.append(NoEscape(r'%sxmin=%.15f, xmax=%.15f,' % (tab_gap, x_min, x_max)))
    doc.append(NoEscape(r'%symin=%.15f, ymax=%.15f,' % (tab_gap, y_min, y_max)))
    doc.append(NoEscape(r'%sxtick=\empty, ytick=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%sxticklabels=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%syticklabels=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%sxlabel=\empty,ylabel=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'%severy axis x label/.style={' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%sat={(ticklabel* cs:1)},' % (tab_gap)))
    doc.append(NoEscape(r'%sanchor=west,' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s},' % (tab_gap)))
    doc.append(NoEscape(r'%severy axis y label/.style={' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%sat={(ticklabel* cs:1)},' % (tab_gap)))
    doc.append(NoEscape(r'%sanchor=south,' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s}' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s]' % (tab_gap)))

def add_q_beta_tikz_main(beta, breakpoints, x_min, x_max, y_min, y_max, y_breakpoints, q, index_str, doc, level, iteration):
    tab_gap = '\t'*level
    if iteration % 2 == 0:
        doc.append(NoEscape(r'%s\begin{figure}[p]' % (tab_gap)))
        level += 1
        tab_gap = '\t'*level
        if not iteration == 0:
            doc.append(NoEscape(r'%s\ContinuedFloat' % (tab_gap)))
        doc.append(NoEscape(r'%s\centering' % (tab_gap)))

    doc.append(NoEscape(r'%s\begin{subfigure}{0.5\linewidth}' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\centering' % (tab_gap)))
    doc.append(NoEscape(r'%s\begin{tikzpicture}[baseline]' % (tab_gap)))
    doc.append(NoEscape(r'%s\begin{axis}' % (tab_gap)))

    add_q_beta_tikz_preamble(x_min, x_max, y_min, y_max, doc, level)
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\addplot[domain=%f:%f, color=blue]{x^%f};' % (tab_gap, x_min, x_max, beta)))
    for index in range(0, len(breakpoints)-1):
        doc.append(NoEscape(r'%s\draw[dotted, thick] (axis cs: %f, %f) -- (axis cs: %f, %f);' % (tab_gap, breakpoints[index], y_breakpoints[index], breakpoints[index+1], y_breakpoints[index+1])))

    doc.append(NoEscape(r'%s\draw[dashed, color=red] (axis cs: %f, %f) -- (axis cs: %f, %f);' % (tab_gap, q, 0, q, pow(q, beta))))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{axis}' % (tab_gap)))
    doc.append(NoEscape(r'%s\end{tikzpicture}' % (tab_gap)))
    doc.append(NoEscape(r'%s\caption{$q^\beta$ - %s}' % (tab_gap, index_str)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{subfigure}%s' % (tab_gap, '%')))
    if iteration % 2 == 1:
        level -= 1
        tab_gap = '\t'*level
        doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))
    return level

def add_q_beta_graphs(instance, active_hx, old_points, doc, level):
    tab_gap = '\t'*level
    beta = instance.Beta.value

    for group in [stream_hx, cu_hx, hu_hx]:
        iteration = 0
        if group == stream_hx:
            index_template = r'$%s$'
            var = instance.q
        elif group == cu_hx:
            index_template = r'$\textit{cu},%s$'
            var = instance.q_cu
        elif group == hu_hx:
            index_template = r'$\textit{hu},%s$'
            var = instance.q_hu
        for active in active_hx[group]:
            breakpoints = old_points[group][q_beta_points][active]
            x_min = 0
            x_max = breakpoints[len(breakpoints)-1]
            y_min = 0
            y_max = pow(x_max, beta)
            y_breakpoints = [pow(q, beta) for q in breakpoints]
            q = var[active].value
            index_str = index_template % (str(active))
            level = add_q_beta_tikz_main(beta, breakpoints, x_min, x_max, y_min, y_max, y_breakpoints, q, index_str, doc, level, iteration)
            iteration += 1
        if iteration % 2 == 1:
            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))

def generate_area_beta_list(area_beta_value, abs_error, rel_error, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
    level +=1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\item Value: %f' % (tab_gap, area_beta_value)))
    doc.append(NoEscape(r'%s\item Error: %.15f' % (tab_gap, abs_error)))
    doc.append(NoEscape(r'%s\item Relative error: %.15f' % (tab_gap, rel_error)))
    level -=1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_area_beta_results(instance, active_hx, old_points, errors, doc, level):
    tab_gap = '\t'*level
    beta = instance.Beta

    for group in [stream_hx, cu_hx, hu_hx]:
        if group == stream_hx:
            section_header = r'$A^\beta$'
            index_template = r'%s'
            var = instance.area_beta
        elif group == cu_hx:
            section_header = r'$A_{CU}^\beta$'
            index_template = r'\textit{cu},%s'
            var = instance.area_cu_beta
        elif group == hu_hx:
            section_header = r'$A_{HU}^\beta$'
            index_template = r'\textit{hu},%s'
            var = instance.area_hu_beta
        if len(active_hx[group]) != 0:
            doc.append(NoEscape(r'%s\subsection{%s}' % (tab_gap, section_header)))
            doc.append(NoEscape(r'%s\begin{itemize}' % (tab_gap)))
            level = level + 1
            tab_gap = '\t'*level
            for active in active_hx[group]:
                index_str = index_template % (str(active))
                area_beta_value = var[active].value
                abs_error = errors[group][area_beta_error][active][absolute_error]
                rel_error = errors[group][area_beta_error][active][relative_error]

                doc.append(NoEscape(r'%s\item $%s$' % (tab_gap, index_str)))
                generate_area_beta_list(area_beta_value, abs_error, rel_error, doc, level)
            level = level - 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{itemize}' % (tab_gap)))

def add_area_beta_tikz_preamble(x_min, x_max, y_min, y_max, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'[' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'axis lines=middle,' % (tab_gap)))
    doc.append(NoEscape(r'xmin=%.15f, xmax=%.15f,' % (tab_gap, x_min, x_max)))
    doc.append(NoEscape(r'ymin=%.15f, ymax=%.15f,' % (tab_gap, y_min, y_max)))
    doc.append(NoEscape(r'xtick=\empty, ytick=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'xticklabels=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'yticklabels=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'xlabel=\empty,ylabel=\empty,' % (tab_gap)))
    doc.append(NoEscape(r'every axis x label/.style={' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'at={(ticklabel* cs:1)},' % (tab_gap)))
    doc.append(NoEscape(r'anchor=west,' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'},' % (tab_gap)))
    doc.append(NoEscape(r'every axis y label/.style={' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'at={(ticklabel* cs:1)},' % (tab_gap)))
    doc.append(NoEscape(r'anchor=south,' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'}' % (tab_gap)))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r']' % (tab_gap)))

def add_area_beta_graphs(instance, active_hx, old_points, doc, level):
    tab_gap = '\t'*level
    beta = instance.Beta
    iteration = 0
    for group in [stream_hx, cu_hx, hu_hx]:
        if group == stream_hx:
            index_template = '%s'
            var = instance.q_beta
        elif group == cu_hx:
            index_template = 'cu,%s'
            var = instance.q_cu_beta
        elif group == hu_hx:
            index_template = 'hu,%s'
            var = instance.q_hu_beta
        for active in active_hx[group]:
            index_str = index_template % (str(active))

            breakpoints = old_points[group][area_q_beta_points][active]
            x_min = 0
            x_max = breakpoints[len(breakpoints)-1]
            diff = x_max - x_min
            delta = diff/30
            y_min = -(1.5*delta)
            y_max = (-1)*y_min
            val = var[active].value

            doc.append(NoEscape(r'%s\begin{figure}[p]' % (tab_gap)))
            level += 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\centering' % (tab_gap)))

            doc.append(NoEscape(r'%s\begin{subfigure}{\linewidth}' % (tab_gap)))
            level += 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\centering' % (tab_gap)))
            doc.append(NoEscape(r'%s\resizebox{\linewidth}{!}{' % (tab_gap)))
            doc.append(NoEscape(r'%s\begin{tikzpicture}' % (tab_gap)))
            doc.append(NoEscape(r'%s\begin{axis}' % (tab_gap)))
            add_num_line_tikz_preamble(x_min, x_max, y_min, y_max, doc, level)
            level += 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\draw (axis cs: %.15f,0) -- (axis cs: %.15f,0);' % (tab_gap, x_min,x_max)))
            for x in breakpoints:
                lval = (tab_gap, x,delta,x,delta)
                doc.append(NoEscape(r'%s\draw (axis cs: %.15f,-%.15f) -- (axis cs: %.15f,%.15f);' % lval))

            doc.append(NoEscape(r'%s\draw[color=red] (axis cs: %.15f,-%.15f) -- (axis cs: %.15f,%.15f);' % (tab_gap, val,1.5*delta,val,1.5*delta)))

            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{axis}' % (tab_gap)))
            doc.append(NoEscape(r'%s\end{tikzpicture}' % (tab_gap)))
            doc.append(NoEscape(r'%s}' % (tab_gap)))
            doc.append(NoEscape(r'%s\caption{$\textit{A}^{\beta}$ - $%s$}' % (tab_gap, index_str)))
            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{subfigure}%s' % (tab_gap, '%')))
            level -= 1
            tab_gap = '\t'*level
            doc.append(NoEscape(r'%s\end{figure}' % (tab_gap)))

def get_breakpoint_list(breakpoints, value):
    same_value = False
    index = 0
    for i in range(0,len(breakpoints)):
        if breakpoints[i] == value:
            same_value = True
            index = i
            break
        elif breakpoints[i] > value:
            index = i-1
            break

    string_breakpoints = [r'$%s$' % str(x) for x in breakpoints]

    if same_value:
        string_breakpoints[index] = r'\textcolor{green}{$%s$}' % (str(breakpoints[index]))
    else:
        string_breakpoints[index] = r'\textcolor{red}{$%s$}' % (str(breakpoints[index]))
        string_breakpoints[index+1] = r'\textcolor{red}{$%s$}' % (str(breakpoints[index+1]))

    return r'$[$%s$]$' % (', '.join(string_breakpoints))

def add_inactive_results_table(results, doc, level):
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\begin{multicols*}{3}' % (tab_gap)))
    doc.append(NoEscape(r'%s\TrickSupertabularIntoMulticols' % (tab_gap)))
    doc.append(NoEscape(r'%s\tablehead{Variable&Value\\\hline}' % (tab_gap)))
    doc.append(NoEscape(r'%s\begin{supertabular}{lr}' % (tab_gap)))
    level += 1
    tab_gap = '\t'*level
    for result in results[1]:
        result_row = result.table_row()
        doc.append(NoEscape(r'%s%s & %s \\' % (tab_gap, result_row[0], result_row[1])))
    level -= 1
    tab_gap = '\t'*level
    doc.append(NoEscape(r'%s\end{supertabular}' % (tab_gap)))
    doc.append(NoEscape(r'%s\end{multicols*}' % (tab_gap)))

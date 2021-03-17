import PJR_TBSLA.pjr.DBHelper as dh
import PJR_TBSLA.pjr.DBRelator as dr
import argparse
import PJR_TBSLA.common.properties as prop
import PJR_TBSLA.common.mpl as plot
import PJR_TBSLA.common.latex as table
import os
import sys
import joblib
import itertools
import sqlite3
import matplotlib as mpl
from my_rcParams import get_rcParams

def append_cmd_to_file(cmd, path):
  with open(path, 'a') as f:
    f.write("\n\n%" + cmd + '\n\n')


def gen_pdf_lf(path, l, f, nr, list_cases):
  mpl.rcParams = get_rcParams()
  filter_dict = {'lang': [l], 'format' : [f], 'NR' : [nr], 'C' : [300]}
  list_sub_cases = ['GR', 'GC', 'LGR', 'LGC', 'BGR', 'BGC', 'CPT']
  COI = 'nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Time (s)', list_cases, False)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  output_file_base = path + f'fig_pangea2_nr{nr}_l'+ l + '_f' + f
  plot.save(fig, output_file_base + '.pdf')
  table.table(m, output_file_base + '.tex', list_cases)
  print(output_file_base + '.pdf')
  con.close()

def gen_pdf_c(path, l, f, nr, list_cases):
  mpl.rcParams = get_rcParams()
  filter_dict = {'lang': [l], 'format' : [f], 'NR' : [nr], 'Q' : [0.4]}
  list_sub_cases = ['GR', 'GC', 'LGR', 'LGC', 'BGR', 'BGC', 'CPT']
  COI = 'nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Time (s)', list_cases, False)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  output_file_base = path + f'fig_pangea2_c_nr{nr}_l'+ l + '_f' + f
  plot.save(fig, output_file_base + '.pdf')
  table.table(m, output_file_base + '.tex', list_cases)
  print(output_file_base + '.pdf')
  con.close()

def gen_pdf_ws(path, l, f, nr, list_cases, nodes, ylabel, yscale):
  mpl.rcParams = get_rcParams()
  filter_dict = {'lang': [l], 'format' : [f], 'C' : [300], 'nodes' : nodes}
  list_sub_cases = ['GR', 'GC', 'LGR', 'LGC', 'BGR', 'BGC', 'CPT']
  COI = 'nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT], [f'nodes,NR,{nr}'])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, STAT, 'Nodes (Cores)', ylabel, list_cases, False, yscale = yscale)
  #fig = plot.plot_ratios_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Weak Scaling Efficiency', list_cases, False)
  #fig = plot.plot_ratios2_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Ratio Tn/T1', list_cases, False)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  output_file_base = path + f'fig_pangea2_ws_nr{nr}_l'+ l + '_f' + f
  plot.save(fig, output_file_base + '.pdf')
  table.table(m, output_file_base + '.tex', list_cases)
  print(output_file_base + '.pdf')
  con.close()


parser = argparse.ArgumentParser()
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
args = parser.parse_args()

CASE_DEF = ['lang', 'format', 'nodes', 'Q', 'GR', 'GC', 'NR', 'NC', 'LGR', 'LGC', 'BGR', 'BGC', 'CPT', 'C']
VOI = 'time_op'
STAT = 'median'
NCPN = 24
PLOTS_OUT = "../chapters/exp_sparse/"
OUTPUT_DB = '.tbsla_db'
INPUT_JSON = 'pangea2_tbsla_YML1x1.json'

FILTER_DICT = {'op': {'a_axpx'}, 'success': {'true'}, 'matrixtype' : {'cqmat'}, 'machine' : {'Pangea2'}}
con = dh.read_json_file(OUTPUT_DB, INPUT_JSON, FILTER_DICT, CASE_DEF, [VOI])
format_list = dh.extract_set(con, 'format')
lang_list = ['MPI', 'YML', 'HPX']
Q_list = sorted(dh.extract_set(con, 'Q'))
con.close()

LxF = list(itertools.product(lang_list, format_list))
list_cases = ['lang', 'format', 'Q']
joblib.Parallel(n_jobs=-1)(joblib.delayed(gen_pdf_lf)(PLOTS_OUT, i[0], i[1], 4000000, list_cases) for i in LxF)
joblib.Parallel(n_jobs=-1)(joblib.delayed(gen_pdf_lf)(PLOTS_OUT, i[0], i[1], 2000000, list_cases) for i in LxF)

list_cases = ['lang', 'format', 'C']
joblib.Parallel(n_jobs=-1)(joblib.delayed(gen_pdf_c)(PLOTS_OUT, i[0], i[1], 4000000, list_cases) for i in LxF)

nodes = [1, 2, 4, 8, 16]
list_cases = ['lang', 'format', 'Q']
joblib.Parallel(n_jobs=-1)(joblib.delayed(gen_pdf_ws)(PLOTS_OUT, i[0], i[1], 4000000, list_cases, nodes, 'Log Time (s)', 'log') for i in LxF)
lang_list = ['MPI', 'HPX']
LxF = list(itertools.product(lang_list, format_list))
joblib.Parallel(n_jobs=-1)(joblib.delayed(gen_pdf_ws)(PLOTS_OUT, i[0], i[1], 3000000, list_cases, nodes, 'Log Time (s)', 'log') for i in LxF)


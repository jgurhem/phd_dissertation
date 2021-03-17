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
import re
import json
from my_rcParams import get_rcParams

def gen_pdf_ss(lang, modifier, nx, ny):
  mpl.rcParams = get_rcParams()
  filter_dict = {'lang': lang, 'nx' : [nx], 'ny' : [ny]}
  list_cases = ['lang']
  list_sub_cases = []
  COI = 'nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Time (s)', list_cases, False)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  output_file_base = PATH_PREFIX + f'fig_pangea2_ss{modifier}_nx{nx}_ny{ny}'
  plot.save(fig, output_file_base + '.pdf')
  table.table(m, output_file_base + '.tex', list_cases)
  con.close()

def gen_pdf_ws(lang, modifier, nx, ny):
  mpl.rcParams = get_rcParams()
  filter_dict = {'lang': lang, 'ny' : [ny]}
  list_cases = ['lang']
  list_sub_cases = []
  COI = 'nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT], [f'nodes,nx,{nx}'])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Time (s)', list_cases, False)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  output_file_base = PATH_PREFIX + f'fig_pangea2_ws{modifier}_nx{nx}_ny{ny}'
  plot.save(fig, output_file_base + '.pdf')
  table.table(m, output_file_base + '.tex', list_cases)
  con.close()


parser = argparse.ArgumentParser()
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
args = parser.parse_args()

CASE_DEF = ['lang', 'nodes', 'nx', 'ny', 'grid_nx', 'grid_ny']
VOI = 'time_mig_max'
STAT = 'median'
NCPN = 24
PATH_PREFIX = "../chapters/exp_kirchhoff/"
OUTPUT_DB = '.km.db'
INPUT_JSON = 'pangea2_km_results.json'

FILTER_DICT = {'app': {'km_dgrid_gen_all'}, 'success': {'true'}, 'machine' : {'Pangea2'}}
con = dh.read_json_file(OUTPUT_DB, INPUT_JSON, FILTER_DICT, CASE_DEF, [VOI])
con.close()

gen_pdf_ss([], '', 15000, 15000)
gen_pdf_ws([], '', 15000, 15000)

gen_pdf_ss(['MPI', 'MPIOMP'], '2', 15000, 15000)
gen_pdf_ws(['MPI', 'MPIOMP'], '2', 15000, 15000)


CASE_DEF = ['op', 'threads', 'cores', 'processes']
OUTPUT_DB = '.km_omp.db'
INPUT_JSON = 'pangea2_km_results_ompi.json'

FILTER_DICT = {}
con = dh.read_json_file(OUTPUT_DB, INPUT_JSON, FILTER_DICT, CASE_DEF, [VOI])

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']
COI = 'threads'
filter_dict = {'op': ['testp1']}
list_cases = ['op']
list_sub_cases = ['cores']
m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
coi_set = sorted(coi_set, key=float)
legend = ['op']
fig = plot.plot_axis(m, coi_set, STAT, 'Threads', 'Time (s)', legend, False)
output_file_base = PATH_PREFIX + f'fig_pangea2_omp_testp1'
plot.save(fig, output_file_base + '.pdf')

row_keys = set()
column_keys = set()
Nval_key = ''
Ncase_key = ''
for v in m.values():
  for k , v in v.items():
    row_keys.add(k)
    for i in v.keys():
      if not i.startswith('__'):
        column_keys.add(i)
      if i.startswith('__') and i.endswith('.Nval'):
        Nval_key = i
      if i.startswith('__') and i.endswith('.Ncase'):
        Ncase_key = i
row_keys = sorted(row_keys)
column_keys = sorted(column_keys)

r = ''
r += '\\begin{tabular}{'
r += 'c' * (len(column_keys) + 1)
r += '}\n\\hline\n'

r += 'Threads'
for i in column_keys:
  r += f'& {i.capitalize()}'
r += '\\\\'
r += '\n\\hline\n'

for k in sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)]):
  v = m[k]
  k_dict = json.loads(k)
  for kr in row_keys:
    r += str(kr)
    for kc in column_keys:
      r += '& ' + str(round(v[kr][kc], 4) if isinstance(v[kr][kc], float) else v[kr][kc])
    r += '\\\\\n'
  r += '\\hline\n'

r += '\\end{tabular}\n'

f = open(output_file_base + '.tex', 'w')
f.write(r)
f.close()

COI = 'processes'
filter_dict = {'op': ['testpm']}
list_cases = ['op']
list_sub_cases = ['threads', 'cores']
m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
coi_set = sorted(coi_set, key=float)
legend = ['op']
fig = plot.plot_axis(m, coi_set, STAT, 'Processes', 'Time (s)', legend, False)
output_file_base = PATH_PREFIX + f'fig_pangea2_omp_testpm'
plot.save(fig, output_file_base + '.pdf')

row_keys = set()
column_keys = set()
Nval_key = ''
Ncase_key = ''
for v in m.values():
  for k , v in v.items():
    row_keys.add(k)
    for i in v.keys():
      if not i.startswith('__'):
        column_keys.add(i)
      if i.startswith('__') and i.endswith('.Nval'):
        Nval_key = i
      if i.startswith('__') and i.endswith('.Ncase'):
        Ncase_key = i
row_keys = sorted(row_keys)
column_keys = sorted(column_keys)

r = ''
r += '\\begin{tabular}{'
r += 'c' * (len(column_keys) + 1)
r += '}\n\\hline\n'

r += 'Processes'
for i in column_keys:
  r += f'& {i.capitalize()}'
r += '\\\\'
r += '\n\\hline\n'

for k in sorted(m.keys(), key = lambda x:[int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)]):
  v = m[k]
  k_dict = json.loads(k)
  for kr in row_keys:
    r += str(kr)
    for kc in column_keys:
      r += '& ' + str(round(v[kr][kc], 4) if isinstance(v[kr][kc], float) else v[kr][kc])
    r += '\\\\\n'
  r += '\\hline\n'

r += '\\end{tabular}\n'

f = open(output_file_base + '.tex', 'w')
f.write(r)
f.close()

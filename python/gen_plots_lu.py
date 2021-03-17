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

def gen_pdf_bar(file_pdf, list_cases, s):
  mpl.rcParams = get_rcParams()
  filter_dict = {'datasize': [s]}
  list_sub_cases = ['nb_blocks', 'nb_proc_per_task']
  COI = 'nb_nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_bar(m, coi_set, STAT, 'Nodes (Cores)', 'Time (s)', list_cases, False)
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  plot.save(fig, file_pdf)
  print(file_pdf)
  con.close()

def gen_pdf_speedup(file_pdf, list_cases, s):
  mpl.rcParams = get_rcParams()
  filter_dict = {'datasize': [s]}
  list_sub_cases = ['nb_blocks', 'nb_proc_per_task']
  COI = 'nb_nodes'
  con = sqlite3.connect(OUTPUT_DB)
  m, coi_set = dr.matrix_relation(con, filter_dict, list_cases, list_sub_cases, COI, VOI, 'auto', [STAT])
  coi_set = sorted(coi_set, key=float)
  fig = plot.plot_ratios_1_on_n_axis(m, coi_set, STAT, 'Nodes (Cores)', 'Time (s)', list_cases, False, yscale='log')
  plot.plot_axis_add_cores_to_node_count(fig, coi_set, NCPN)
  plot.save(fig, file_pdf)
  print(file_pdf)
  con.close()

parser = argparse.ArgumentParser()
parser.add_argument('-pv', help='Print values for the figure', dest='pv', default=False, action='store_true')
args = parser.parse_args()

CASE_DEF = ['machine', 'test', 'datasize', 'nb_cores', 'nb_nodes', 'lang', 'blocksize', 'nb_blocks', 'nb_proc_per_task']
VOI = 'time_calc'
STAT = 'mean'
NCPN = 16
OUTPUT_DB = '.tbdla_db'
INPUT_JSON = 'all_results.json'

FILTER_DICT = {'success': {'true'}, 'machine' : {'Poincare'}, 'test' : {'blockLU'}}
con = dh.read_json_file_raw(OUTPUT_DB, INPUT_JSON)
cur = con.cursor()
query = 'UPDATE auto_all_values SET nb_nodes = nb_nodes - 1 WHERE lang is "YML+XMP"'
cur.execute(query)
con.commit()
dh.create_filter(con, 'auto', FILTER_DICT)
dh.create_case_table(con, 'auto', CASE_DEF)
dh.compute_stats(con, 'auto', VOI)

list_cases = ['lang']
gen_pdf_bar('../chapters/exp_dense/fig_strong_scaling_bar_task.pdf', list_cases, 16384)
gen_pdf_bar('../chapters/exp_dense/fig_strong_scaling_bar_task_32k.pdf', list_cases, 32768)
gen_pdf_bar('../chapters/exp_dense/fig_strong_scaling_bar_task_49k.pdf', list_cases, 49152)

gen_pdf_speedup('../chapters/exp_dense/fig_strong_scaling_speedup_task.pdf', list_cases, 16384)
gen_pdf_speedup('../chapters/exp_dense/fig_strong_scaling_speedup_task_32k.pdf', list_cases, 32768)
gen_pdf_speedup('../chapters/exp_dense/fig_strong_scaling_speedup_task_49k.pdf', list_cases, 49152)


python3 gen_plots_lu.py
python3 gen_plots_km.py
python3 gen_plots_tbsla.py

python3 Graph_Generator/lu.py -n 4 --fontsize 80 > lu.dot
dot lu.dot -Tpdf -o ../chapters/exp_dense/lu_graph_n4.pdf

python3 Graph_Generator/sls_g.py -n 4 --fontsize 80 > sls_g.dot
dot sls_g.dot -Tpdf -o ../chapters/exp_dense/sls_g_graph_n4.pdf

python3 Graph_Generator/sls_gj.py -n 4 --fontsize 80 > sls_gj.dot
dot sls_gj.dot -Tpdf -o ../chapters/exp_dense/sls_gj_graph_n4.pdf

python3 Graph_Generator/sls_lu.py -n 4 --fontsize 80 > sls_lu.dot
dot sls_lu.dot -Tpdf -o ../chapters/exp_dense/sls_lu_graph_n4.pdf

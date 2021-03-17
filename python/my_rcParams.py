import matplotlib as mpl

def get_rcParams():
  myrcParams = mpl.rcParams.copy()
  myrcParams['font.family'] = 'serif'
  myrcParams['font.serif'] = ['Times New Roman']
  myrcParams['font.size'] = 10
  return myrcParams

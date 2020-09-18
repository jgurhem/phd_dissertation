import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random

nr = 30
nc = 30
c = 4
q = 0.05

random.seed(1234)
A = np.zeros([nr, nc])

for i in range(nr):
  for j in range(c):
    if i + j < nc:
      A[i, i + j] = 1

for i in range(nr):
  for j in range(c):
    if i + j < nc:
      r = random.randrange(0, 1000)
      if r / 1000 < q:
        r = random.randrange(0, nc)
        while A[i, r] == 1:
          r = random.randrange(0, nc)
        A[i, r] = 1
        A[i, i + j] = 0

fig, ax = plt.subplots()
im = ax.imshow(A, cmap='Greys')
ax.tick_params(bottom=False, left=False, labelleft=False, labelbottom=False)
ax.patch.set_edgecolor('black')
ax.patch.set_linewidth('2')
fig.savefig("chapters/methods/cqmat.pdf", bbox_inches="tight")
plt.close()



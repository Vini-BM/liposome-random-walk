'''
@ Vinícius Müller
Created: 01-07-2024

Plots a histogram of the walkers' final positions obtained from 'liposome.py'
'''

# Imports
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# LaTeX
plt.rcParams.update({
    'font.family': 'serif',
    'mathtext.fontset': 'cm'
})

# Parameters
N = 10000
t = 15000
m_list = [100,1000,10000] # m values (for m=10 all particles were removed)

# Histogram
fig, axes = plt.subplots(nrows=1,ncols=3,figsize=(12,6)) # initialize plot

for m, ax in zip(m_list,axes):
    file = glob(f'randw-position_N{N}_m{m}_t{t}_*.dat')[0] # get first file that matches pattern, independent of seed
    walkers, positions = np.loadtxt(file,unpack=True)
    ax.hist(positions,bins=int(m/4),density=True)
    ax.set_xlim(0,1)
fig.supxlabel(r'$x$')
fig.supylabel(r'$\rho$')
fig.suptitle(rf'Particle density inside liposome at $t={t}$ | $N_0 = {N}$')
plt.show()

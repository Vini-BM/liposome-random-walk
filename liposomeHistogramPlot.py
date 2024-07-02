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
# Parameters
N = 10000
params_list = [(100,30000,30),(1000,75000,60),(10000,200000,75)] # (m, tmax, bins)

# Histogram
fig, axes = plt.subplots(nrows=1,ncols=3,figsize=(16,6)) # initialize plot
plt.subplots_adjust(left=0.075,right=0.95)

for params, ax in zip(params_list,axes):
    m, t, bins = params
    files = glob(f'files/randw-position_N{N}_m{m}_t{t}_*.dat')
    positions = []
    for file in files:
        walkers, pos = np.loadtxt(file,unpack=True)
        positions.extend(pos)
    ax.hist(positions,bins=bins,density=True)
    ax.set_xlim(0,1)
    ax.set_title(rf'$m = {m}$ | $t_{{max}} = {t}$ | ${len(files)}$ samples')
fig.supxlabel(r'$x$')
fig.supylabel(r'$\rho$')
fig.suptitle(rf'Particle density inside liposome at $t_{{max}}$ | $N_0 = {N}$')
plt.savefig('plots/liposomeHistogram.png', dpi=300)
plt.show()

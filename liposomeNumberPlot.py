'''
@ Vinícius Müller
Created: 27-03-2024
Last updated: 01-07-2024

Plots the number of walkers inside the liposome as a function of time, using data from 'liposome.py'.
Calculates the decay exponent by fitting the data.
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

def get_tau(m):
    '''
    Returns the theoretical decay exponent
    '''
    return 8*m**2/np.pi**2

# Parameters
N = 10000
params_list = [(10,10000),(100,30000),(1000,50000),(10000,150000)] # (m, tmax)

# Number of particles
fig, axes = plt.subplots(nrows=2,ncols=2,figsize=(12,6)) # initialize plot
axes = [axes[0][0],axes[0][1],axes[1][0],axes[1][1]] # linearize axes for accessing through loop

for params, ax in zip(params_list,axes):
    m, t = params
    file = glob(f'randw-number_N{N}_m{m}_t{t}_*.dat')[0] # get first file that matches pattern, independent of seed
    tau = get_tau(m)
    time, num_walkers = np.loadtxt(file,unpack=True)
    decay = N*np.exp(-time/tau) # theoretical decay
    ax.plot(time,num_walkers)
    #ax.plot(time,decay,ls='--')
    ax.set_xlim(time[0],time[-1])
    ax.set_yscale('log')
    ax.set_title(rf'$m = {m}$')

fig.supxlabel(r'$t$')
fig.supylabel(r'$N$')
fig.suptitle(rf'Number of particles inside liposome | $N_0 = {N}$')
plt.show()
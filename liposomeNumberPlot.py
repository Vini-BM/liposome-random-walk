'''
@ Vinícius Müller
Created: 27-03-2024
Last updated: 01-07-2024

Plots the number of walkers inside the liposome as a function of time, using data from 'liposome.py'.
Calculates the decay exponent by fitting the data.
Also returns a text file containing the numerical exponent for each value of m.
'''

# Imports
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
#from scipy.optimize import curve_fit
from scipy.stats import linregress

# LaTeX
plt.rcParams.update({
    'font.family': 'serif',
    'mathtext.fontset': 'cm'
})

def get_tau(m):
    '''
    Returns the theoretical decay exponent.
    '''
    return 8*m**2/np.pi**2

def decay_fit(x,tau,constant):
    '''
    Returns the exponential decay for fitting data.
    '''
    return constant*np.exp(-x/tau)

# Parameters
N = 10000
params_list = [(10,1000,100),(100,30000,3000),(1000,75000,30000),(10000,200000,70000)] # (m, tmax, start)
tau_list = [] # list for storing the numerical and theoretical exponent

# Number of particles
fig, axes = plt.subplots(nrows=2,ncols=2,figsize=(14,8)) # initialize plot
plt.subplots_adjust(left=0.1,right=0.95)
axes = [axes[0][0],axes[0][1],axes[1][0],axes[1][1]] # linearize axes for accessing through loop

for params, ax in zip(params_list,axes):

    # Parameters
    m, t, start = params
    if m == 10:
        end = 800
    else:
        end = -1
    print(t)
    theor_tau = get_tau(m) # theoretical value of exponent

    # Plot data
    files = glob(f'files/randw-number_N{N}_m{m}_t{t}_*.dat')
    num_walkers = []
    for file in files:
        time, walkers = np.loadtxt(file,unpack=True)
        num_walkers.append(walkers)
    #print(len(walkers))
    num_walkers = np.mean(num_walkers,axis=0)
    #print(np.shape(num_walkers))
    num_walkers /= N # normalize
    ax.plot(time,num_walkers,label='Data')

    # Fit data
    log_num = np.log(num_walkers)
    fit = linregress(time[start:end],log_num[start:end]) # linear fit on ln(N(t))
    num_tau = -1/fit.slope # numerical exponent
    const = np.exp(fit.intercept) # multiplicative constant
    tau_list.append((num_tau,theor_tau)) # storing values for table

    # Plot fit
    fit_data = decay_fit(time[start:end],num_tau,const)
    ax.plot(time[start:end],fit_data,label=rf'Fit, $\tau_{{num}} = {num_tau:.3f}$',ls='--')

    # Axis attributes
    ax.set_xlim(0,t)
    ax.set_yscale('log')
    ax.set_title(rf'$m = {m}$ | Mean of ${len(files)}$ samples')
    ax.legend()

fig.supxlabel(r'$t$')
fig.supylabel(r'$N/N_0$')
fig.suptitle(rf'Number of particles inside liposome | $N_0 = {N}$')
#plt.savefig(f'plots/liposomeNumberWalkers.png', dpi=300)
plt.show()

# Text file with table
with open(f'files/numerical_tau_N{N}.txt', 'w') as output:
    output.write(f"# {'m':<6}      numerical        theoretical    {'relative error':>15} \n")
    for params, tau in zip(params_list,tau_list):
        m = params[0]
        num_tau, theor_tau = tau
        error = np.abs(theor_tau - num_tau)/theor_tau
        output.write(f'{m:<6}  {num_tau:15.3f}  {theor_tau:15.3f}  {error:>16.3f} \n')
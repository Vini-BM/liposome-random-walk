# Liposome random walk

Simulation of a liposome breaking with an one-dimensional random walk.

## Setup
$N$ walkers are confined on $x = [0,1)$; the boundary conditions are such that there is a wall at $x = 0$ and a drain at $x = 1$. Space is discretized with $m$ divisions such that the walker's step is $l = 1/m$.

## Problem
We intend to study the exponential behavior of the number of particles *inside* the liposome as a function of time. To do so, we intend to obtain the $\tau_{num}$ exponent through the simulation and compare it with the theoretical value obtained for a diffusion process:

$$\tau_{theor} = \frac{4L^2}{D\pi^2}$$

where $D = \frac{l^2}{2\bar{t}}$ is the diffusion constant and $\bar{t}$ is the time between steps. In this case, $\bar{t} = 1$ MCS (Monte Carlo Step) and $L = 1$. Therefore, we may write

$$\tau_{theor} = \frac{8}{l^2 \pi^2} = \frac{8m^2}{\pi^2}$$

## Scripts and files

Script ```liposome.py``` contains the main program. It runs the simulation for $N$ particles for $m \in \{10,100,1000,10000\}$. The simulation time is chosen empirically as:

    * $t_{max} = 10000$ for $m = 10$;
    * $t_{max} = 30000$ for $m = 100$;
    * $t_{max} = 50000$ for $m = 1000$;
    * $t_{max} = 150000$ for $m = 10000$.

$N$ may be given as an argument when calling the script; if not, the program will run with the default value $N = 10000$.

Each run uses a random 'global' seed for the PRNG and the $i^{\text{th}}$ walker has a unique seed given by $\text{seed} + 20*i$. The output of each run is a file of the form ```randw-number_*.dat``` containing the number of particles (walkers) inside the liposome at every instant, and a file of the form ```randw-position_*.dat``` containing the positions of all particles at the end of the walk.
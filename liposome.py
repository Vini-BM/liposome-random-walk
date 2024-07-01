'''
@ Vinícius Müller
Created: 27-03-2024
Last updated: 01-07-2024

Simulates the liposome breaking with random walkers.
'''

# Imports
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import sys
from secrets import randbits

# Walker Class
class LiposomeWalker:

    def __init__(self,seed,step_len):
        self.step = step_len # step length
        self.rng = rd.Random(seed) # private RNG
        self.x = self.rng.random() # initial position
        self.state = 1 # 1: walker inside liposome, 0: walker outside liposome

    def move(self):
        if self.state == 1: # only move if inside
            r = self.rng.random()
            if r <= 0.5 and self.x - self.step > 0: # wall at x=0
                self.x -= self.step # left
            else:
                self.x += self.step # right
                if self.x > 1:
                    self.state = 0 # outside liposome


# Main
def main(N=10000):
    '''
    Performs a random walk subject to the boundary conditions of the liposome problem
    Creates N objects of LiposomeWalker class
    Space interval: 0 < x < 1
    Wall at x=0
    Drain at x=1

    Arguments:
        N: number of particles/walkers

    Fixed parameters:
        m: interval division -> list of values
        tmax: walk time
    '''

    # Initialization
    #m_list = [10,100,1000,10000] # interval division
    #tmax_list = [1000,30000,50000,200000] # walk time
    m_list = [10000]
    tmax_list = [200000]

    # Loop over m
    for m, tmax in zip(m_list,tmax_list):
        print(m) # control
        step = 1/m # step length
        seed = randbits(32) # random global seed for walkers
        walkerlist = [LiposomeWalker(seed+20*i,step) for i in range(N)] # list of walkers
        ## each walker has a unique seed generated from the same 'global' seed

        # Output files
        fileN = f'files/randw-number_N{N}_m{m}_t{tmax}_{seed}.dat'
        fileX = f'files/randw-position_N{N}_m{m}_t{tmax}_{seed}.dat'

        # Walk
        with open(fileN,'w') as outN:
            t = 0 # initialize time
            outN.write('# time    number of walkers \n')
            outN.write(f'{t}    {N} \n') # initial condition
            while t < tmax: # loop
                for walker in walkerlist:
                    walker.move() # move walkers
                    if walker.state == 0:
                        walkerlist.remove(walker) # remove outside walkers from list
                num = len(walkerlist) # number of walkers inside
                t += 1 # Monte Carlo Step
                outN.write(f'{t}    {num} \n')

        # Histogram of final positions
        with open(fileX,'w') as outX:
            outX.write('# walker    position \n')
            for i in range(len(walkerlist)):
                x = walkerlist[i].x # walker position after tf MCS
                outX.write(f'{i}    {x} \n')

if __name__ == '__main__':
    try: # custom arguments
        N = int(sys.argv[1])
        main(N)
    except IndexError: # default arguments
        main()
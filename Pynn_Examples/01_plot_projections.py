"""
Script for plotting projections in PyNN
(adapted from example in Brian2 tutorial)

Author: Shailesh Appukuttan, CNRS
Date: September 2017
"""

import sys
from pyNN.utility import get_script_args

import numpy
import matplotlib.pyplot as plt

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

dt = 0.1
setup(min_delay = dt, timestep = dt)

SIZE = 10
v_rest = -60.0
pop1 = Population(SIZE, IF_curr_exp(v_rest=v_rest))
pop2 = Population(SIZE, IF_curr_exp(v_rest=v_rest))
pop1.initialize(v=v_rest)
pop2.initialize(v=v_rest)

# Use one of the below
myprj = Projection(pop1, pop2, FixedProbabilityConnector(0.2), StaticSynapse())
#myprj = Projection(pop1, pop2, FixedProbabilityConnector(0.8), StaticSynapse())
#myprj = Projection(pop1, pop2, AllToAllConnector(), StaticSynapse())
#myprj = Projection(pop1, pop2, OneToOneConnector(), StaticSynapse())

def visualise_connectivity(prj):
    weights = prj.get(["weight"], format="list")
    preList = [i[0] for i in weights]
    postList = [i[1] for i in weights]
    Ns = len(prj.pre)
    Nt = len(prj.post)

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.plot(numpy.zeros(Ns), numpy.arange(Ns), 'ok', ms=10)
    plt.plot(numpy.ones(Nt), numpy.arange(Nt), 'ok', ms=10)
    for i, j in zip(preList, postList):
        plt.plot([0, 1], [i, j], '-k')
    plt.xticks([0, 1], ['Source', 'Target'])
    plt.ylabel('Neuron index')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-1, max(Ns, Nt))
    plt.subplot(122)
    plt.plot(preList, postList, 'ok')
    plt.xlim(-1, Ns)
    plt.ylim(-1, Nt)
    plt.xlabel('Source neuron index')
    plt.ylabel('Target neuron index')
    plt.show(block=True)

visualise_connectivity(myprj)

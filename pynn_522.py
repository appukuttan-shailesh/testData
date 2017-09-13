import sys
from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

dt = 0.1
setup(min_delay = dt, timestep = dt)

v_rest = -60.0
cells = Population(2, IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0, v_rest=v_rest))
cells.initialize(v=v_rest)

#prj = Projection(cells, cells, AllToAllConnector(), StaticSynapse(weight=[0.123]))
prj = Projection(cells, cells, AllToAllConnector(), StaticSynapse())
prj.set(weight= [1,2,3,4])

print "Weights = ", prj.get(["weight"], format="list")

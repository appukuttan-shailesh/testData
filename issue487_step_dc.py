import sys
from pyNN.utility import get_script_args
from nose.tools import assert_true
from numpy import isclose

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

sim_dt = 0.1
setup(min_delay=1.0, timestep = sim_dt)

v_rest = -60.0
cells = Population(2, IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0, v_rest=v_rest))
cells.initialize(v=v_rest)

dcsource = DCSource(amplitude=0.10, start=25.0, stop=125.0)
cells[0].inject(dcsource)

step = StepCurrentSource(times=[25.0, 75.0, 125.0], amplitudes=[0.05, 0.10, 0.20])
cells[1].inject(step)

cells.record('v')

runtime = 100.0

run(runtime)
run(runtime)
"""
run(runtime*2)
"""

vm = cells.get_data().segments[0].filter(name="v")[0]
end()
v_dc = vm[:, 0]
v_step = vm[:, 1]

if '--plot-figure' in sys.argv:

    import matplotlib.pyplot as plt
    plt.ion()
    plt.plot(vm.times, v_dc, 'r')
    plt.plot(vm.times, v_step, 'b')
    plt.xlabel("time (ms)")
    plt.ylabel("Vm (mV)")
    plt.legend()
    plt.axvline(x=25.0, c='k')
    plt.axvline(x=75.0, c='k')
    plt.axvline(x=125.0, c='k')

    plt.suptitle(simulator_name, fontsize=25)
    plt.show(block=True)  # SA: changed

end()

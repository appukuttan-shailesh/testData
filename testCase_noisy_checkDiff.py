"""
Simple test of injecting noisy current into a cell
"""
import sys
from pyNN.utility import get_script_args, normalized_filename

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

setup(timestep = 0.01, min_delay=1.5)

filename = normalized_filename("Results", "NoisyCurrentInput", "pkl", simulator_name)

cells = Population(1, IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0))

mean=0.55
stdev=0.1
start=50.0
stop=125.0
inj_dt = 0.01

noise1 = NoisyCurrentSource(mean=mean, stdev=stdev, start=start, stop=stop, dt=inj_dt)
cells[0].inject(noise1)

record('v', cells, filename, annotations={'script_name': __file__})

run(200.0)

if '--plot-figure' in sys.argv:

    import matplotlib.pyplot as plt
    plt.ion()
    vm = cells.get_data().segments[0].filter(name="v")[0]

    plt.plot(vm.times, vm)
    plt.xlabel("time (ms)")
    plt.ylabel("Vm (mV)")
    for i in numpy.arange(start, stop, inj_dt):
        plt.axvline(x=i, ls='--', c='r')
    plt.axvline(x=stop, c='k')
    plt.legend()

    plt.show(block=True)  # SA: changed

end()

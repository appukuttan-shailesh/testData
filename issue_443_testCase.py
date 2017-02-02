"""
Simple test of injecting various types of current into a cell
"""
import sys
from pyNN.utility import get_script_args, normalized_filename

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

setup()

filename = normalized_filename("Results", "NoisyCurrentInput", "pkl", simulator_name)

cells = Population(3, IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0))

mean=0.55
stdev=0.1
start=50.0
stop=125.0

steady = DCSource(amplitude=mean, start=start, stop=stop)
cells[0].inject(steady)

noise1 = NoisyCurrentSource(mean=mean, stdev=stdev, start=start, stop=stop, dt=10)
cells[1].inject(noise1)

acsource = ACSource(start=start, stop=stop, amplitude=mean, offset=0.0, frequency=100.0, phase=0.0)
cells[2].inject(acsource)

record('v', cells, filename, annotations={'script_name': __file__})

run(200.0)

if '--plot-figure' in sys.argv:

    import matplotlib.pyplot as plt
    plt.ion()
    vm = cells.get_data().segments[0].filter(name="v")[0]

    plt.figure(figsize=(8,4))
    plt.plot(vm.times, vm)
    plt.xlabel("time (ms)")
    plt.ylabel("Vm (mV)")
    plt.legend()
    plt.axvline(x=start, c='r')
    plt.axvline(x=stop, c='r')
    plt.show(block=True)  # SA: changed

end()

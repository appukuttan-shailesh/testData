"""
Simple test of injecting current into a cell and recording the current profile
"""
import sys
from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

#setup()
setup(min_delay=0.1)

cells = Population(4, IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0))

mean=0.55
stdev=0.1
start=50.0
stop=125.0

acsource = ACSource(start=start, stop=stop, amplitude=mean, offset=0.0, frequency=100.0, phase=0.0)
cells[0].inject(acsource)
acsource.record()

dcsource = DCSource(amplitude=mean, start=start, stop=stop)
cells[1].inject(dcsource)
dcsource.record()

noise = NoisyCurrentSource(mean=mean, stdev=stdev, start=start, stop=stop, dt=1.0)
cells[2].inject(noise)
noise.record()

step = StepCurrentSource(times=[start, (start+stop)/2, stop], amplitudes=[0.4, 0.6, 0.2])
cells[3].inject(step)
step.record()

cells.record('v')

run(200.0)

i_ac = acsource.get_data()
i_t_ac = i_ac.times.magnitude
i_dc = dcsource.get_data()
i_t_dc = i_dc.times.magnitude
i_noise = noise.get_data()
i_t_noise = i_noise.times.magnitude
i_step = step.get_data()
i_t_step = i_step.times.magnitude

if '--plot-figure' in sys.argv:

    import matplotlib.pyplot as plt
    plt.ion()
    vm = cells.get_data().segments[0].filter(name="v")[0]
    v_ac = vm[:, 0]
    v_dc = vm[:, 1]
    v_noise = vm[:, 2]
    v_step = vm[:, 3]

    plt.figure(figsize=(8,8))

    plt.subplot(2,1,1)
    plt.plot(vm.times, v_ac, 'r')
    plt.plot(vm.times, v_dc, 'b')
    plt.plot(vm.times, v_noise, 'g')
    plt.plot(vm.times, v_step, 'k')
    plt.xlabel("time (ms)")
    plt.ylabel("Vm (mV)")
    plt.legend()
    plt.axvline(x=start, c='r')
    plt.axvline(x=stop, c='r')

    plt.subplot(2,1,2)
    plt.plot(i_t_ac, i_ac, 'r')
    plt.plot(i_t_dc, i_dc, 'b')
    plt.plot(i_t_noise, i_noise, 'g')
    plt.plot(i_t_step, i_step, 'k')
    plt.xlim(min(i_t_ac), max(i_t_ac))
    plt.xlabel("time (ms)")
    plt.ylabel("current (nA)")
    plt.legend()
    plt.axvline(x=start, c='m')
    plt.axvline(x=stop, c='m')

    plt.show(block=True)  # SA: changed

end()

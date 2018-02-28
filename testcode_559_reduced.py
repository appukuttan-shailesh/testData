from pyNN.utility import get_script_args
from importlib import import_module
import matplotlib.pyplot as plt

simulator_name = get_script_args(1)[0]
sim = import_module("pyNN.%s" % simulator_name)

tstop = 500.0
#time_step = 0.005

for time_step in [0.005, 0.05, 0.01, 0.1]:
    sim.setup(timestep=time_step, debug=True)
    cell_params5a = {'tau_refrac': 2.0, 'a': 0, 'tau_m': 16.8, 'e_rev_E': 0.0, 'i_offset': 0.15, 'cm': 0.12, 'delta_T': 2, 'e_rev_I': -75.0, 'v_thresh': -50.0, 'b': 0, 'tau_syn_E': 1.0, 'v_reset': -60.0, 'v_spike': 0.0, 'tau_syn_I': 1.0, 'tau_w': 144.0, 'v_rest': -70.0}
    pop_EIF_cond_alpha_isfa_ista = sim.Population(1, sim.EIF_cond_alpha_isfa_ista(**cell_params5a), label="pop_EIF_cond_alpha_isfa_ista")
    pop_EIF_cond_alpha_isfa_ista.record('v')
    pop_EIF_cond_alpha_isfa_ista.record('spikes')

    sim.run(tstop)
    sim.end()

    data = pop_EIF_cond_alpha_isfa_ista.get_data()
    vm = data.segments[0].analogsignals[0]
    ts = [t*time_step/1000. for t in range(len(vm))]
    plt.plot(ts, vm, '-', label='time_step = %s ms'%time_step)

plt.title("Simulator: %s"%simulator_name)
plt.legend()
plt.show()

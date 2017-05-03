import nest
import numpy as np
import pylab as pl

# quite badly written code
# could easily be condensed if I was more aware of NEST syntax

# create neuron
neuron_noise = nest.Create('iaf_cond_alpha', params = {'V_reset': -65.0})

 # create multimeters
m_Vm_noise = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})
m_Inj_noise = nest.Create('multimeter', params = {'record_from': ['I'], 'interval' :0.1})

# Create generators and connect
noise = nest.Create('noise_generator', 1, params = {'mean'  : 450.0,
                    'std' : 50.0, 'dt' : 1.0, 'std_mod' : 25.0,
                    'phase' : 45.0, 'frequency' : 50.0,
                    'origin' : 5.0, 'start' : 2.5, 'stop' : 40.0})

nest.Connect(noise, neuron_noise)
nest.Connect(m_Vm_noise, neuron_noise)
nest.Connect(m_Inj_noise, noise)

# simulate
nest.Simulate(50)

# obtain and display data
events_Vm_noise = nest.GetStatus(m_Vm_noise)[0]['events']
t_Vm_noise = events_Vm_noise['times'];

events_Inj_noise = nest.GetStatus(m_Inj_noise)[0]['events']
t_Inj_noise = events_Inj_noise['times'];

pl.subplot(211)
pl.plot(t_Vm_noise, events_Vm_noise['V_m'], 'r')
pl.xlabel('Time [ms]')
pl.ylabel('Membrane potential [mV]')

pl.subplot(212)
pl.plot(t_Inj_noise, events_Inj_noise['I'], 'b')
pl.xlabel('Time [ms]')
pl.ylabel('Injected Current [pA]')

pl.show(block=True)

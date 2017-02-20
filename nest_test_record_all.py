import nest
import numpy as np
import pylab as pl

# quite badly written code
# could easily be condensed if I was more aware of NEST syntax

# create neuron
neuron_ac = nest.Create('iaf_cond_alpha', params = {'V_reset': -65.0})
neuron_dc = nest.Create('iaf_cond_alpha', params = {'V_reset': -65.0})
neuron_step = nest.Create('iaf_cond_alpha', params = {'V_reset': -65.0})
neuron_noise = nest.Create('iaf_cond_alpha', params = {'V_reset': -65.0})

 # create multimeters
m_Vm_ac = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})
m_Vm_dc = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})
m_Vm_step = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})
m_Vm_noise = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})

m_Inj_ac = nest.Create('multimeter', params = {'record_from': ['I'], 'interval' :0.1})
m_Inj_dc = nest.Create('multimeter', params = {'record_from': ['I'], 'interval' :0.1})
m_Inj_step = nest.Create('multimeter', params = {'record_from': ['I'], 'interval' :0.1})
m_Inj_noise = nest.Create('multimeter', params = {'record_from': ['I'], 'interval' :0.1})

# Create generators and connect
ac = nest.Create('ac_generator', 1, params = {'amplitude': 500.0, 'frequency': 50.0, 'phase' : 45.0, 'origin' : 5.0, 'start' : 2.5, 'stop'  : 40.0})
nest.Connect(ac, neuron_ac)
nest.Connect(m_Vm_ac, neuron_ac)
nest.Connect(m_Inj_ac, ac)

dc = nest.Create('dc_generator', 1, params = {'amplitude'  : 500.0, 'origin' : 5.0, 'start' : 2.5, 'stop'  : 40.0})
nest.Connect(dc, neuron_dc)
nest.Connect(m_Vm_dc, neuron_dc)
nest.Connect(m_Inj_dc, dc)

step_times = [10.0, 20.0, 25.0, 30.0]
step_currents = [500.0, 250.0, 100.0, 400.0]
params = { "amplitude_times": step_times, "amplitude_values":step_currents, 'origin' : 5.0, 'start' : 2.5, 'stop'  : 40.0}
step = nest.Create("step_current_generator", 1, params)
nest.Connect(step, neuron_step)
nest.Connect(m_Vm_step, neuron_step)
nest.Connect(m_Inj_step, step)

noise = nest.Create('noise_generator', 1, params = {'mean'  : 450.0, 'std' : 50.0, 'dt' : 0.1, 'std_mod' : 25.0, 'phase' : 45.0, 'frequency' : 50.0, 'origin' : 5.0, 'start' : 2.5, 'stop'  : 40.0})
nest.Connect(noise, neuron_noise)
nest.Connect(m_Vm_noise, neuron_noise)
nest.Connect(m_Inj_noise, noise)



# simulate
nest.Simulate(50)

# obtain and display data
events_Vm_ac = nest.GetStatus(m_Vm_ac)[0]['events']
t_Vm_ac = events_Vm_ac['times'];
events_Vm_dc = nest.GetStatus(m_Vm_dc)[0]['events']
t_Vm_dc = events_Vm_dc['times'];
events_Vm_step = nest.GetStatus(m_Vm_step)[0]['events']
t_Vm_step = events_Vm_step['times'];
events_Vm_noise = nest.GetStatus(m_Vm_noise)[0]['events']
t_Vm_noise = events_Vm_noise['times'];

events_Inj_ac = nest.GetStatus(m_Inj_ac)[0]['events']
t_Inj_ac = events_Inj_ac['times'];
events_Inj_dc = nest.GetStatus(m_Inj_dc)[0]['events']
t_Inj_dc = events_Inj_dc['times'];
events_Inj_step = nest.GetStatus(m_Inj_step)[0]['events']
t_Inj_step = events_Inj_step['times'];
events_Inj_noise = nest.GetStatus(m_Inj_noise)[0]['events']
t_Inj_noise = events_Inj_noise['times'];

pl.subplot(211)
pl.plot(t_Vm_ac, events_Vm_ac['V_m'], 'r')
pl.plot(t_Vm_dc, events_Vm_dc['V_m'], 'b')
pl.plot(t_Vm_step, events_Vm_step['V_m'], 'k')
pl.plot(t_Vm_noise, events_Vm_noise['V_m'], 'g')
pl.xlabel('Time [ms]')
pl.ylabel('Membrane potential [mV]')

pl.subplot(212)
pl.plot(t_Inj_ac, events_Inj_ac['I'], 'r')
pl.plot(t_Inj_dc, events_Inj_dc['I'], 'b')
pl.plot(t_Inj_step, events_Inj_step['I'], 'k')
pl.plot(t_Inj_noise, events_Inj_noise['I'], 'g')
pl.xlabel('Time [ms]')
pl.ylabel('Injected Current [pA]')

pl.show(block=True)

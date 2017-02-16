import nest
import numpy as np
import pylab as pl

# create neuron and multimeter
neuron = nest.Create('iaf_cond_alpha')

m_Vm = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})
m_Inj = nest.Create('multimeter', params = {'record_from': ['amplitude'], 'interval' :0.1})

# Create generator and connect
sine = nest.Create('ac_generator', 1, {'amplitude': 5.0, 'frequency': 100.0})
nest.Connect(sine, neuron)
nest.Connect(m_Vm, neuron)
nest.Connect(m_Inj, sine)

# simulate
nest.Simulate(50)

# obtain and display data
events_Vm = nest.GetStatus(m_Vm)[0]['events']
t_Vm = events_Vm['times'];
events_Inj = nest.GetStatus(m_Inj)[0]['events']
t_Inj = events_Inj['times'];

pl.subplot(211)
pl.plot(t_Vm, events_Vm['V_m'])
pl.xlabel('Time [ms]')
pl.ylabel('Membrane potential [mV]')

pl.subplot(212)
pl.plot(t_Inj, events_Inj['amplitude'], 'r')
pl.xlabel('Time [ms]')
pl.ylabel('Injected Current [pA]')

pl.show(block=True)

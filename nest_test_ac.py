import nest
import numpy as np
import pylab as pl

# create neuron
neuron_ac = nest.Create('iaf_cond_alpha', params = {'V_reset': -65.0})
#nest.SetStatus(neuron_ac, "V_m", -65.0)

 # create multimeters
m_Vm_ac = nest.Create('multimeter', params = {'record_from': ['V_m'], 'interval' :0.1})
m_Inj_ac = nest.Create('multimeter', params = {'record_from': ['I'], 'interval' :0.1})

# Create generators and connect
ac = nest.Create('ac_generator', 1, params = {'amplitude': 550.0,
                                              'offset': 1000.0,
                                              'frequency': 100.0,
                                              'phase' : 180.0, 'origin' : 2.5,
                                              'start' : 2.5, 'stop' : 40.0})
nest.Connect(ac, neuron_ac)
nest.Connect(m_Vm_ac, neuron_ac)
nest.Connect(m_Inj_ac, ac)

# simulate
nest.Simulate(25)

# obtain and display data
events_Vm_ac = nest.GetStatus(m_Vm_ac)[0]['events']
t_Vm_ac = events_Vm_ac['times'];
events_Inj_ac = nest.GetStatus(m_Inj_ac)[0]['events']
t_Inj_ac = events_Inj_ac['times'];

print t_Inj_ac[48:55]
print events_Inj_ac['I'][48:55]
print t_Vm_ac[58:65]
print events_Vm_ac['V_m'][58:65]

print "Length t", len(t_Inj_ac)
print "Length I", len(events_Inj_ac['I'])
print "Length V", len(events_Vm_ac['V_m'])

pl.axhline(y=1000.0)
pl.axvline(x=5.0)
pl.plot(t_Inj_ac, events_Inj_ac['I'], 'r', linewidth=2)
pl.xlabel('Time [ms]')
pl.ylabel('Injected Current [pA]')

pl.show(block=True)

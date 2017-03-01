from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

repeats = 2
dt = 0.1
simtime = 100
setup(timestep=dt, min_delay=dt)
p = Population(1, IF_curr_exp())
#c = DCSource(amplitude=0.0)
c = DCSource(amplitude=0.0, start=25.0, stop=50.0)
p[0].inject(c)
p.record('v')

for i in range(repeats):
    run(simtime)
    c.amplitude += 0.1

data = p.get_data().segments[0].analogsignalarrays[0]
end()

import matplotlib.pyplot as plt
plt.figure(figsize=(6,3))
plt.plot(data.times, data)
plt.xlim(min(data.times), max(data.times))
plt.xlabel("time (ms)")
plt.ylabel("Vm (mV)")
plt.tight_layout()
plt.show(block=True)

print data[int(simtime / dt), 0]
print data[-1, 0]
print int(simtime / dt)
print data.times[int(simtime / dt)]

# check that the value of v just before increasing the current is less than
# the value at the end of the simulation
assert data[int(simtime / dt), 0] < data[-1, 0]

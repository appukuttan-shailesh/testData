from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

dt = 0.1
setup(timestep=dt, min_delay=dt)
p = Population(1, IF_curr_exp())
c = DCSource(amplitude=0.5)
c.inject_into(p)
p.record('v')

simtime = 200.0
# run(200.0)    #doesn't fail
run(100.0)
run(100.0)

v = p.get_data().segments[0].filter(name="v")[0]

# check that the length of vm vector is as expected theoretically
print "len(v) = ", len(v)
print "(int((simtime*repeats)/dt) + 1) = ", (int(simtime/dt) + 1)
print "min(t) = ", min(v.times)
print "max(t) = ", max(v.times)
assert (len(v) == (int(simtime/dt) + 1))

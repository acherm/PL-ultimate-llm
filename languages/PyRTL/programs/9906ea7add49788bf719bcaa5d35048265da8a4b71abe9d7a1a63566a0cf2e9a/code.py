import pyrtl

# Create a simple counter
counter = pyrtl.Register(8, 'counter')
counter.next <<= counter + 1

# Simulate the counter
sim = pyrtl.Simulation()
for cycle in range(10):
    sim.step({})
    print('Cycle %d: counter = %d' % (cycle, sim.inspect('counter')))

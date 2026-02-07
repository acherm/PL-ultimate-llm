from myhdl import Signal, delay, always, now, Simulation

def ClkDriver(clk):
    halfPeriod = delay(10)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk

def Counter(clk, count, enable):
    @always(clk.posedge)
    def logic():
        if enable:
            count.next = (count + 1) % 16

    return logic

clk = Signal(0)
count = Signal(0)
enable = Signal(1)

clk_driver = ClkDriver(clk)
counter = Counter(clk, count, enable)

sim = Simulation(clk_driver, counter)
sim.run(100)
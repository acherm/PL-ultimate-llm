from nmigen import *
from nmigen.back.pysim import *


class Counter(Elaboratable):
    def __init__(self, width):
        self.v = Signal(width, reset=2**width - 1)
        self.o = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.v.eq(self.v - 1)
        m.d.comb += self.o.eq(self.v[-1])
        return m


if __name__ == "__main__":
    dut = Counter(16)
    with Simulator(dut) as sim:
        sim.add_clock(1e-6)

        def process():
            for _ in range(100):
                yield

        sim.add_sync_process(process)
        sim.run()

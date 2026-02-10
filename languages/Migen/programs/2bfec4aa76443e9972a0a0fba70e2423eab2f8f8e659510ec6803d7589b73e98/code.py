from migen import *

class Counter(Module):
    def __init__(self, width=8):
        self.count = Signal(width)
        self.ce = Signal()

        self.sync += [
            If(self.ce,
                self.count.eq(self.count + 1)
            )
        ]

if __name__ == "__main__":
    dut = Counter(width=16)
    print(verilog.convert(dut, ios={dut.count, dut.ce}))

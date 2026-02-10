import smartpy as sp

@sp.module
def main():
    class Counter(sp.Contract):
        def __init__(self):
            self.data.count = 0

        @sp.entrypoint
        def increment(self):
            self.data.count += 1

        @sp.entrypoint
        def decrement(self):
            self.data.count -= 1

        @sp.entrypoint
        def reset(self):
            self.data.count = 0

@sp.add_test()
def test():
    scenario = sp.test_scenario("Counter", main)
    c1 = main.Counter()
    scenario += c1
    c1.increment()
    scenario.verify(c1.data.count == 1)
    c1.increment()
    scenario.verify(c1.data.count == 2)
    c1.decrement()
    scenario.verify(c1.data.count == 1)
    c1.reset()
    scenario.verify(c1.data.count == 0)

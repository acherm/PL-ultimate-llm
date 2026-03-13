from Numberjack import *

N = 8
queens = VarArray(N, N)
model = Model(
    AllDiff(queens),
    AllDiff([queens[i]+i for i in range(N)]),
    AllDiff([queens[i]-i for i in range(N)])
)
solver = model.load('Mistral')
solver.solve()
print([queens[i].get_value() for i in range(N)])

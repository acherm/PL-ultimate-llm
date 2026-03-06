from copperhead import *
import copperhead.runtime.cuda_support as cuda

@cu
def saxpy(a, x, y):
    return map(lambda xi, yi: a * xi + yi, x, y)

@cu
def sum_of_squares(x):
    return reduce(lambda a, b: a + b,
                  map(lambda xi: xi * xi, x))

with cuda:
    a = 2.0
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [10.0, 20.0, 30.0, 40.0, 50.0]
    result = saxpy(a, x, y)
    print(list(result))
    total = sum_of_squares(x)
    print(total)

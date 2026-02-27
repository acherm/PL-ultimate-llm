#pythran export dpsum(float64[])

def dpsum(arr):
    s = 0.0
    for i in range(len(arr)):
        s += arr[i]
    return s

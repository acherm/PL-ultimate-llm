import numpy as np

# IPython magic commands demo
# %timeit measures execution time
# This script uses IPython API directly

from IPython import get_ipython
from IPython.core.magic import register_line_magic

@register_line_magic
def greet(name):
    print(f"Hello, {name}!")

# Fibonacci using numpy for performance
def fib(n):
    a, b = np.uint64(0), np.uint64(1)
    result = []
    for _ in range(n):
        result.append(int(a))
        a, b = b, a + b
    return result

print("Fibonacci sequence (first 10):")
print(fib(10))

# Demonstrate IPython display utilities
from IPython.display import display, HTML
display(HTML("<b>IPython display system</b>"))

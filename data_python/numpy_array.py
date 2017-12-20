import numpy as np

"""
Demonstrates ndarray attributes.

Run from the commandline with 

python arrayattribute
"""

b = np.arange(24).reshape(2, 12)
print("In: b")
print(b)

print("In: b.ndim")
print(b.ndim)

print("In: b.size")
print(b.size)

print("In: b.itemsize")
print(b.itemsize)

print(b)
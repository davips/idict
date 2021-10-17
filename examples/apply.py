# Lazily applying functions to idict
from idict import idict

a = idict(x=3)
print(a)
# ...

a = a >> idict(y=5) >> {"z": 7} >> (lambda x, y, z: {"r": x ** y // z})
print(a)
# ...

print(a.r)
# ...

print(a)
# ...

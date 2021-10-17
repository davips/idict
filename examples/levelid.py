# Identity example
from idict import idict

a = idict(x=3)
print(a)
# ...

b = idict(y=5)
print(b)
# ...

print(a >> b)
# ...

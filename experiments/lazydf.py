from numpy import array
from pandas import DataFrame, Series

a = array([1, 2, 3])
b = array([5, 6, 7])
sa=Series(a.data)
sb=Series(b.data)
print(sa)
print(sb)
print()
a[2]=7777

df = DataFrame({"a": sa, "b": sb})
print(df)

print()
a[1] = 99999
print("df", df)

print()
a = sa.array
print(a)
a[0]=99999999999999999


print()
print(df)
print()
print()
print()
import pyarrow as pa

# Convert from pandas to Arrow
table = pa.Table.from_pandas(df)
# Convert back to pandas
df_new = table.to_pandas()

# Infer Arrow schema from pandas
schema = pa.Schema.from_pandas(df)
print("===========================")
print(df)
print()
print(table)
print()
print(df_new)
print()
print(schema)



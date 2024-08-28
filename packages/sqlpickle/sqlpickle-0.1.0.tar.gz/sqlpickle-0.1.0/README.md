# SQL Pickle

SQL Pickle is a simple key-value store that uses SQLite to store pickled objects.

```python
from sqlpickle import KeyValueStore
store = KeyValueStore('test.db')

store['test'] = 1
print(store['test']) 
# 1

store['very_complex_object'] = {'a': 1, 'b': 2}
```

# Memoization

```python
from sqlpickle import memoize, KeyValueStore

@memoize(KeyValueStore('test.db'))
def expensive_function(x):
    return x**2

expensive_function(2) # 4
expensive_function(2) # 4
```

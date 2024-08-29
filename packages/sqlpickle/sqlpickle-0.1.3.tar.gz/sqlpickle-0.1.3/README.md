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

# Other features

```python
'key' in store # True
store.keys() # ['key1', 'key2']
store.items() # [('key1', 1), ('key2', 2)]
store.get('key1') # 1
store.get('key2') # 2
store.get('key3') # KeyError
len(store) # 2
store.random_keys(2) # ['key1', 'key2']
```
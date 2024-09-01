# pythonz_enum

implementation of rust-like value holding enums

# example

```python
from pythonz_enum import Maybe

def find(predicate, iter_):
    try:
        return Maybe.Just(next(filter(predicate, iter_)))
    except StopIteration:
        return Maybe.Nothing()
    
find(lambda a: a is not None, [None, 2, 3])  # Maybe.Just(2)
```
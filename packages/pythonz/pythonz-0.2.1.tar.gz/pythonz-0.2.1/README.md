# pythonz

pythonz is a package to make your python coding experience more powerful.

# example

```python
from functools import partial
from pythonz import pipe, symbol, Maybe

__empty__ = symbol("empty")


def find(fn, itr, default=__empty__):
    try:
        return (
                pipe(itr)
                / partial(filter, fn)
                / next
                // Maybe.just
        )
    except StopIteration:
        if default is __empty__:
            return Maybe.nothing()
        return Maybe.just(default)


# a = pipe(5).and_then(range).then_finally(list) 
a = pipe(5) / range // list  # [0, 1, 2, 3, 4] 
b = find(lambda x: x % 2 == 1, a).unwrap()  # 1
c = find(lambda x: x > 4, a)  # Maybe.None()
```


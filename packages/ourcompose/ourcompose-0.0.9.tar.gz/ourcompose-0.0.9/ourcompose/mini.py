import inspect
from functools import wraps
from typing import Optional, List
from graphlib import TopologicalSorter
from itertools import starmap

def piecify(depends_on: Optional[List[str]] = None, log: bool = False):
    def inner(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            if log:
                print(f"Running {fn.__class__.__name__}.{fn.__name__} with args {args} and kwargs {kwargs}")
            return fn(self, *args, **kwargs)
        
        setattr(wrapper, 'dependencies', depends_on or [])
        return wrapper
    return inner

def pipeline(cls):
    
    def execute(self, extract: Optional[str] = None):
        # Get all the pieces
        pieces = dict(
            filter(
                lambda x: hasattr(x[1], 'dependencies'),
                inspect.getmembers(
                    self, 
                    predicate=inspect.ismethod,
                )
            )
        )

        result = {}
        for name in TopologicalSorter(
            dict(
                starmap(
                    lambda name, fn: (
                        name,
                        fn.dependencies
                    ),
                    pieces.items()
                )
            )
        ).static_order():
            fn = pieces[name]
            args = [
                result[dep] 
                for dep in fn.dependencies
            ]
            result[name] = fn(*args)

        if extract:
            return result[extract]
        else:
            return result[name]
        
    setattr(cls, 'execute', execute)
    
    return cls
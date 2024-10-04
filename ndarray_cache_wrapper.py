from functools import lru_cache, wraps
import numpy as np

def ndarray_cache(*args, **kwargs):
    def decorator():
        @wraps(function)
        def wrapper(nd_array, *args, **kwargs):
            hashable_array = array_to_tuple(nd_array)
            return cached_wrapper(hashable_array, *args, **kwargs)
        
        @lru_cache(*args, **kwargs)
        def cached_wrapper(hashable_array, *args, **kwargs):
            array = np.asarray(hashable_array)
            return function(array, *args, **kwargs)
        
        def array_to_tuple(nd_array):
            try:
                return (tuple(array_to_tuple(_)) for _ in nd_array)
            except TypeError:
                return nd_array
        
        # lru_cache attributes
        wrapper.cache_info = cached_wrapper.cache_info
        wrapper.cache_clear = cached_wrapper.cache_clear

        return wrapper
    return decorator
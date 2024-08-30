import functools

import tensorflow as tf

# FUNCTIONS ###################################################################

compose = lambda __l: (lambda __x: functools.reduce(lambda __e, __f: __f(__e), __l, __x))

distribute = lambda __f: (lambda *__t: tuple(map(__f, __t)))

# AXES ########################################################################

def normalize_dim(dim: int) -> int:
    return -1 if (dim is None or dim < 0) else dim

def multiply_dim(dim_l: int, dim_r: int) -> int:
    return -1 if (dim_l == -1 or dim_r == -1) else dim_l * dim_r

def divide_dim(dim_l: int, dim_r: int) -> int:
    return -1 if (dim_l == -1 or dim_r == -1) else dim_l // dim_r

# SHAPES ######################################################################

def normalize_shape(shape: list) -> list:
    return [normalize_dim(dim=__d) for __d in list(shape)]

def filter_shape(shape: list, axes: list) -> list:
    __shape = normalize_shape(shape)
    __axes = [__a % len(__shape) for __a in axes] # interpret negative indexes
    return [__d if __i in __axes else 1 for __i, __d in enumerate(__shape)]

def divide_shape(shape: list, input_axis: int, output_axis: int, factor: int, insert: bool=False) -> list:
    # copy
    __shape = normalize_shape(shape)
    # rank, according to the new shape
    __rank = len(__shape) + int(insert)
    # axes, taken from the new shape
    __axis0 = input_axis % __rank
    __axis1 = output_axis % __rank
    # option to group data on a new axis
    if insert: __shape.insert(__axis1, 1)
    # move data from axis 0 to axis 1
    __shape[__axis0] = divide_dim(__shape[__axis0], factor)
    __shape[__axis1] = multiply_dim(__shape[__axis1], factor)
    # return
    return __shape

def merge_shape(shape: list, left_axis: int, right_axis: int, left: bool=True) -> list:
    # copy
    __shape = normalize_shape(shape)
    __rank = len(__shape)
    # normalize (negative indexes)
    __axis_l = left_axis % __rank
    __axis_r = right_axis % __rank
    # new dimension
    __dim = multiply_dim(__shape[__axis_l], __shape[__axis_r])
    # select axes
    __axis_k = __axis_l if left else __axis_r # kept axis
    __axis_d = __axis_r if left else __axis_l # deleted axis
    # new shape
    __shape[__axis_k] = __dim
    __shape.pop(__axis_d)
    # return
    return __shape

def merge_to_same_rank(x1: tf.Tensor, x2: tf.Tensor) -> tuple:
    # init
    __x1, __x2 = x1, x2
    __s1, __s2 = list(__x1.shape), list(__x2.shape)
    __r1, __r2 = len(__s1), len(__s2)
    # x1 has one more axis
    if __r1 == __r2 + 1:
        __s1 = merge_shape(shape=__s1, left_axis=-2, right_axis=-1, left=True)
        __x1 = tf.reshape(__x1, shape=__s1)
    # x2 has one more axis
    if __r2 == __r1 + 1:
        __s2 = merge_shape(shape=__s2, left_axis=-2, right_axis=-1, left=True)
        __x2 = tf.reshape(__x2, shape=__s2)
    # return both
    return __x1, __x2

# CACHE #######################################################################

def create_cache(batch_dim: int, cache_dim: int, head_dim: int, num_heads: int=None) -> tf.Tensor:
    __shape = [2, batch_dim, cache_dim, num_heads, head_dim] if num_heads else [2, batch_dim, cache_dim, head_dim]
    return tf.zeros(__shape, dtype=tf.float32)

def update_cache(tensor: tf.Tensor, cache: tf.Tensor, axis: int=1, step: int=None) -> tf.Tensor:
    if step is not None:
    	# expand the sequence axis with 1-dim axes
        __shape = filter_shape(shape=list(cache.shape), axes=[axis])
        # index of the updated row
        __indices = tf.reshape(tf.one_hot(indices=step, depth=__shape[axis], dtype=tensor.dtype), shape=__shape)
        # updated cache
        __tensor = cache + tensor * __indices
    else:
        __tensor = tf.concat(values=[tf.cast(cache, tensor.dtype), tensor], axis=axis)
    # past + current values
    return __tensor
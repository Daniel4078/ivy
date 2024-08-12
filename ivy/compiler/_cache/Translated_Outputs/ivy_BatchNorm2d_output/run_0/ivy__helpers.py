import functools
import ivy
import re


def ivy_handle_methods(fn):
    def extract_function_name(s):
        match = re.search("_(.+?)(?:_\\d+)?$", s)
        if match:
            return match.group(1)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if ivy.is_array(args[0]):
            return fn(*args, **kwargs)
        else:
            pattern = "_bknd_|_bknd|_frnt_|_frnt"
            fn_name = extract_function_name(re.sub(pattern, "", fn.__name__))
            new_fn = getattr(args[0], fn_name)
            return new_fn(*args[1:], **kwargs)

    return wrapper


def ivy_empty_frnt(
    *args,
    size=None,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    pin_memory=False,
    memory_format=None,
):
    if args and size:
        raise TypeError("empty() got multiple values for argument 'shape'")
    if size is None:
        size = (
            args[0]
            if isinstance(args[0], (tuple, list, ivy.Shape, ivy.NativeShape))
            else args
        )
    if isinstance(size, (tuple, list)):
        size = tuple(s.to_scalar() if ivy.is_array(s) else s for s in size)
    return ivy.empty(shape=size, dtype=dtype, device=device, out=out)


def ivy_zeros_frnt(
    *args, size=None, out=None, dtype=None, device=None, requires_grad=False
):
    if args and size:
        raise TypeError("zeros() got multiple values for argument 'shape'")
    if size is None:
        size = (
            args[0]
            if isinstance(args[0], (tuple, list, ivy.Shape, ivy.NativeShape))
            else args
        )
    return ivy.zeros(shape=size, dtype=dtype, device=device, out=out)


def ivy_ones_frnt(
    *args, size=None, out=None, dtype=None, device=None, requires_grad=False
):
    if args and size:
        raise TypeError("ones() got multiple values for argument 'shape'")
    if size is None:
        size = (
            args[0]
            if isinstance(args[0], (tuple, list, ivy.Shape, ivy.NativeShape))
            else args
        )
    return ivy.ones(shape=size, dtype=dtype, device=device, out=out)


def ivy_tensor_frnt(
    data, *, dtype=None, device=None, requires_grad=False, pin_memory=False
):
    return ivy.array(data, dtype=dtype, device=device)


def ivy_zeros_like_frnt(
    input,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None,
):
    ret = ivy.zeros_like(input, dtype=dtype, device=device)
    return ret


def ivy_zero__frnt_(arr):
    ret = ivy_zeros_like_frnt(arr)
    arr = ivy.inplace_update(arr, ret).data
    return arr


def ivy_full_like_frnt(
    input,
    fill_value,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None,
):
    fill_value = ivy.to_scalar(fill_value)
    return ivy.full_like(input, fill_value, dtype=dtype, device=device)


def ivy_fill__frnt_(arr, value):
    ret = ivy_full_like_frnt(arr, value, dtype=arr.dtype, device=arr.device)
    arr = ivy.inplace_update(arr, ret).data
    return arr


def ivy__no_grad_fill_(tensor, val):
    return ivy_fill__frnt_(tensor, val)


def ivy_ones_(tensor):
    return ivy__no_grad_fill_(tensor, 1.0)


def ivy__no_grad_zero_(tensor):
    return ivy_zero__frnt_(tensor)


def ivy_zeros_(tensor):
    return ivy__no_grad_zero_(tensor)


def ivy_device_frnt(dev):
    return ivy.default_device(dev)


@ivy_handle_methods
def ivy_split_frnt(tensor, split_size_or_sections, dim=0):
    if isinstance(split_size_or_sections, int):
        split_size = split_size_or_sections
        split_size_or_sections = [split_size] * (tensor.shape[dim] // split_size)
        if tensor.shape[dim] % split_size:
            split_size_or_sections.append(tensor.shape[dim] % split_size)
    return tuple(
        ivy.split(
            tensor,
            num_or_size_splits=split_size_or_sections,
            axis=dim,
            with_remainder=True,
        )
    )


@ivy_handle_methods
def ivy_split_frnt_(arr, split_size, dim=0):
    return ivy_split_frnt(arr, split_size, dim)


@ivy_handle_methods
def ivy_add_frnt(input, other, *, alpha=1, out=None):
    return ivy.add(input, other, alpha=alpha, out=out)


@ivy_handle_methods
def ivy_add_frnt_(arr, other, *, alpha=1):
    return ivy_add_frnt(arr, other, alpha=alpha)


def ivy_add__frnt_(arr, other, *, alpha=1):
    arr = ivy_add_frnt_(arr, other, alpha=alpha)
    return arr


def ivy_batch_norm_frnt(
    input,
    running_mean,
    running_var,
    weight=None,
    bias=None,
    training=False,
    momentum=0.1,
    eps=1e-05,
):
    normalized, mean, var = ivy.batch_norm(
        input,
        running_mean,
        running_var,
        offset=bias,
        scale=weight,
        training=training,
        eps=eps,
        momentum=momentum,
        data_format="NSC",
    )
    if training:
        ivy.inplace_update(running_mean, mean).data
        ivy.inplace_update(running_var, var).data
    return normalized


def ivy_dim_frnt_(arr):
    return arr.ndim

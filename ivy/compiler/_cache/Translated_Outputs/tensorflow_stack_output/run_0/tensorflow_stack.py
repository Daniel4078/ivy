import tensorflow

from typing import Optional
from typing import List
from typing import Tuple
from typing import Union


def tensorflow_stack(
    arrays: Union[Tuple[tensorflow.Tensor], List[tensorflow.Tensor]],
    /,
    *,
    axis: int = 0,
    out: Optional[Union[tensorflow.Tensor, tensorflow.Variable]] = None,
):
    try:
        return tensorflow.experimental.numpy.stack(arrays, axis)
    except ValueError as e:
        raise Exception(e) from e

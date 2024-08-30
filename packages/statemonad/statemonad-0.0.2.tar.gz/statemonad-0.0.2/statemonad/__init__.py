from collections.abc import Iterable

from statemonad.statemonad.statemonad import StateMonad as _StateMonad
from statemonad.statemonad.from_ import from_ as _from_, get as _get, put as _put
from statemonad.statemonad.init import init_state_monad as _init_state_monad

from_ = _from_
get = _get
put = _put

from_node = _init_state_monad


def zip[State, U](
    monads: Iterable[_StateMonad[State, U]],
):
    """
    Combine multiple state monads into a single monad that evaluates each
    one and returns their result as a tuple.

    This function takes an iterable of state monads and produces a new state monad
    that, when applied to a state, runs each of the original monads in sequence
    with the same initial state. The final state is derived from the sequence, and
    the result is a tuple of all the values produced by the monads.

    Example:
    ``` python
    m1, m2, m3 = from_(1), from_(2), from_(3)

    state, value = zip((m1, m2, m3)).apply(state)

    print(value)  # Output will be (1, 2, 3)
    ```
    """

    monads_iterator = iter(monads)
    try:
        current = next(monads_iterator).map(lambda v: (v,))
    except StopIteration:
        return from_[State](tuple[U]())
    else:
        for other in monads_iterator:
            current = current.zip(other).map(lambda v: v[0] + (v[1],))
        return current

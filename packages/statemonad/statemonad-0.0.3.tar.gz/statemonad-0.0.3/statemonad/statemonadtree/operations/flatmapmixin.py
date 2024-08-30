from abc import abstractmethod
from typing import Callable

from statemonad.exceptions import StateMonadOperatorException
from statemonad.statemonadtree.nodes import SingleChildStateMonadNode, StateMonadNode
from statemonad.utils.getstacklines import FrameSummaryMixin, to_operator_exception_message

class FlatMapMixin[State, U, ChildU](FrameSummaryMixin, SingleChildStateMonadNode[State, U, ChildU]):
    def __str__(self) -> str:
        return f'flat_map({self.child}, {self.func.__name__})'

    @property
    @abstractmethod
    def func(self) -> Callable[[ChildU], StateMonadNode[State, U]]: ...

    def apply(self, state: State) -> tuple[State, U]:
        state, value = self.child.apply(state)

        try:
            result = self.func(value).apply(state)
            
        except StateMonadOperatorException:
            raise

        except Exception:
            raise StateMonadOperatorException(
                to_operator_exception_message(stack=self.stack)
            )

        return result

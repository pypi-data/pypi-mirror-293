from statemonad.statemonadtree.nodes import TwoChildrenStateMonadNode


class ZipMixin[State, L, R](TwoChildrenStateMonadNode[State, tuple[L, R], L, R]):
    def __str__(self) -> str:
        return f'zip({self.left}, {self.right})'

    def apply(self, state: State) -> tuple[State, tuple[L, R]]:
        state, left = self.left.apply(state)
        state, right = self.right.apply(state)

        return state, (left, right)

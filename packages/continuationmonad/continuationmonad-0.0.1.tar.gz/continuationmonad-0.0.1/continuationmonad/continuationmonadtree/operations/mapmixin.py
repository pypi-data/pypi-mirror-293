from abc import abstractmethod
from typing import Callable

from continuationmonad.continuationmonadtree.nodes import SingleChildContinuationMonadNode
from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.utils.getstacklines import FrameSummaryMixin, to_operator_exception_message


class MapMixin[U, ChildU](FrameSummaryMixin, SingleChildContinuationMonadNode[U, ChildU]):
    def __str__(self) -> str:
        return f'map({self.child}, {self.func})'

    @property
    @abstractmethod
    def func(self) -> Callable[[ChildU], U]:
        ...

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, U], Continuation]
    ) -> Continuation:
        def n_on_next(n_trampoline: Trampoline, value: ChildU):
            try:
                n_value = self.func(value)

            except ContinuationMonadOperatorException:
                raise

            except Exception:
                raise ContinuationMonadOperatorException(
                    to_operator_exception_message(stack=self.stack)
                )

            return on_next(n_trampoline, n_value)
        
        return self.child.subscribe(trampoline, n_on_next)

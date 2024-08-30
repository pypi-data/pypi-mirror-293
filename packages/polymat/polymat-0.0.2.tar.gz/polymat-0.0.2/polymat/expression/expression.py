from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, override

from polymat.expressiontree.expressiontree import (
    SingleChildExpressionTreeMixin,
    ExpressionTree,
)
from polymat.expressiontree.init import (
    init_addition,
    init_assert_polynomial,
    init_assert_vector,
    init_block_diagonal,
    init_cache,
    init_combinations,
    init_diag,
    init_differentiate,
    init_elementwise_mult,
    init_eval,
    init_filter,
    init_from_or_none,
    init_from_,
    init_kron,
    init_linear_monomials,
    init_linear_in,
    init_matrix_mult,
    init_product,
    init_quadratic_in,
    init_quadratic_monomials,
    init_rep_mat,
    init_reshape,
    init_get_item,
    init_sum,
    init_symmetric,
    init_transpose,
    init_v_stack,
    init_variable_vector,
)
from polymat.expressiontree.operations.filtermixin import FilterMixin
from polymat.expressiontree.operations.productmixin import ProductMixin
from polymat.sparserepr.sparserepr import SparseRepr
from polymat.state import State
from polymat.utils.getstacklines import FrameSummary, get_frame_summary
from polymat.symbol import Symbol
from polymat.utils import typing


class Expression(SingleChildExpressionTreeMixin, ABC):
    def __add__(self, other: typing.FROM_TYPES):
        return self._binary(init_addition, self, other)

    def __getitem__(self, key):
        assert len(key) == 2

        return self.copy(
            child=init_get_item(
                child=self.child,
                key=key,
            )
        )

    def __matmul__(self, other: typing.FROM_TYPES):
        return self._binary(init_matrix_mult, self, other)

    def __mul__(self, other: typing.FROM_TYPES):
        return self._binary(init_elementwise_mult, self, other)

    def __neg__(self):
        return (-1) * self

    def __pow__(self, exponent: int):
        result = self
        for _ in range(exponent - 1):
            result = result * self
        return result

    def __radd__(self, other: typing.FROM_TYPES):
        return self._binary(init_addition, other, self)

    def __rmul__(self, other: typing.FROM_TYPES):
        return self._binary(init_elementwise_mult, other, self)

    def __rmatmul__(self, other: typing.FROM_TYPES):
        return self._binary(init_matrix_mult, other, self)

    def __rsub__(self, other: typing.FROM_TYPES):
        return other + (-self)

    def __str__(self):
        return str(self.child)

    def __sub__(self, other: typing.FROM_TYPES):
        return self + (-other)

    def __truediv__(self, other: float | int):
        if not isinstance(other, float | int):
            return NotImplementedError

        return (1 / other) * self

    def _is_left_subtype_of_right(self, left, right):
        # overwrite this function when extending Expression
        return False

    def _binary(self, op, left, right) -> Expression:
        stack = get_frame_summary(index=4)

        if isinstance(left, Expression) and isinstance(right, Expression):
            child = op(left.child, right.child, stack)

            if self._is_left_subtype_of_right(left, right):
                return right.copy(child=child)
            else:
                return left.copy(child=child)

        elif isinstance(left, Expression):
            right = init_from_or_none(right, stack)

            if right is None:
                return NotImplemented

            return left.copy(child=op(left.child, right, stack))

        # else right is an Expression
        else:
            left = init_from_or_none(left, stack)

            if left is None:
                return NotImplemented

            return right.copy(child=op(left, right.child, stack))

    def _get_children(
        self, others: Iterable[Expression], stack: tuple[FrameSummary, ...]
    ) -> tuple[ExpressionTree, ...]:
        if isinstance(others, Expression):
            others = (others,)

        def gen_children():
            yield self.child

            for e in others:
                if isinstance(e, Expression):
                    expr = e.child
                else:
                    expr = init_from_(e, stack=stack)

                yield expr

        # arrange blocks vertically and concatanete
        return tuple(gen_children())

    def _v_stack(
        self, others: Iterable[Expression], stack: tuple[FrameSummary, ...]
    ) -> ExpressionTree:
        # """ Vertically stack expressions """
        return init_v_stack(
            children=self._get_children(others, stack=stack),
            stack=get_frame_summary(),
        )

    @override
    def apply(self, state: State) -> tuple[State, SparseRepr]:
        return self.child.apply(state)

    def assert_vector(self, stack=get_frame_summary()):
        return self.copy(child=init_assert_vector(stack=stack, child=self))

    def assert_polynomial(self, stack=get_frame_summary()):
        return self.copy(child=init_assert_polynomial(stack=stack, child=self))

    def block_diag(self, others: Iterable[Expression]):
        stack = get_frame_summary()

        return self.copy(
            child=init_block_diagonal(
                children=self._get_children(others, stack=stack),
            )
        )

    def cache(self):
        return self.copy(child=init_cache(self, stack=get_frame_summary()))

    # only applies to vector
    def combinations(self, degrees: tuple[int, ...]):
        return self.copy(
            child=init_combinations(
                child=self.child,
                degrees=degrees,
                stack=get_frame_summary(),
            )
        )

    @abstractmethod
    def copy(self, /, **changes) -> Expression: ...

    # only applies to symmetric matrix or vector
    def diag(self):
        return self.copy(
            child=init_diag(
                child=self.child,
                stack=get_frame_summary(),
            )
        )

    def diff(self, variables: Expression):
        return self.copy(
            child=init_differentiate(
                child=self.child,
                variables=variables,
                stack=get_frame_summary(),
            )
        )

    def eval(self, substitutions: dict[Symbol, tuple[float, ...]]):
        return self.copy(
            child=init_eval(
                child=self.child,
                substitutions=substitutions,
                stack=get_frame_summary(),
            )
        )

    # only applies to vector
    def filter(self, predicator: FilterMixin.PREDICATOR_TYPE):
        return self.copy(
            child=init_filter(
                child=self.child,
                predicator=predicator,
                stack=get_frame_summary(),
            )
        )

    def h_stack(self, others: Iterable[Expression]):
        return self.T.v_stack((e.T for e in others)).T

    def kron(self, other: Expression):
        return self.copy(child=init_kron(left=self.child, right=other.child))

    # only applies to vector
    def linear_in(
        self,
        variables: Expression,
        monomials: Expression | None = None,
    ):
        return self.copy(
            child=init_linear_in(
                child=self.child,
                monomials=monomials,
                variables=variables,
                stack=get_frame_summary(),
            )
        )

    def linear_monomials_in(self, variables: Expression):
        return self.copy(
            child=init_linear_monomials(
                child=self.child,
                variables=variables,
            )
        )

    def product(self, others: Iterable[Expression], degrees: ProductMixin.DEGREE_TYPES):
        stack = get_frame_summary()

        return self.copy(
            child=init_product(
                children=self._get_children(others, stack=stack),
                stack=stack,
                degrees=degrees,
            )
        )

    # only applies to polynomial
    def quadratic_in(
        self,
        variables: Expression,
        monomials: Expression | None = None,
    ):
        return self.copy(
            child=init_symmetric(
                child=init_quadratic_in(
                    child=self.child,
                    monomials=monomials,
                    variables=variables,
                    stack=get_frame_summary(),
                )
            )
        )

    def quadratic_monomials_in(self, variables: Expression):
        return self.copy(
            child=init_quadratic_monomials(
                child=self.child,
                variables=variables,
            )
        )

    def rep_mat(self, n: int, m: int):
        return self.copy(
            child=init_rep_mat(
                child=self.child,
                repetition=(n, m),
            ),
        )

    def reshape(self, n: int, m: int):
        return self.copy(
            child=init_reshape(
                child=self.child,
                new_shape=(n, m),
            )
        )

    def sum(self):
        """
        sum all elements of each row
        """

        return self.copy(
            child=init_sum(
                child=self.child,
            )
        )

    def symmetric(self):
        return self.copy(child=init_symmetric(child=self.child))

    @property
    def T(self):
        return self.copy(child=init_transpose(self.child))

    def to_monomial_vector(self):
        return self.assert_vector(stack=get_frame_summary())

    def to_polynomial(self):
        return self.assert_polynomial(stack=get_frame_summary())[0, 0]

    def to_variable_vector(self):
        return self.copy(
            child=init_variable_vector(
                child=self.child,
            )
        )

    def to_vector(self):
        return self.assert_vector(stack=get_frame_summary())

    def trace(self):
        return self.diag().T.sum()

    def v_stack(self, others: Iterable[Expression]):
        stack = get_frame_summary()
        return self.copy(child=self._v_stack(others=others, stack=stack))

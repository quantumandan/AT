from dataclasses import dataclass, asdict
import json
from typing import *
from .category import Morphism


@dataclass
class iNull:
    """
    Represents the multiplicative annihilator of an algebra.

    The value of iNull is arbitrary so long as its hashable because it doesn't matter what
    symbol labels "zero" so long as it performs the role of multiplicative annihilator AND
    the additive identity. A extremely important detail is that different algebras may have
    a different value for the origin of a projective coordinate system. So the origin must
    be a shared property of overlapping algebraic components.

    The `iNull.__eq__` method serves to enforce a local diffeomorphism constraint, which is a
    necessary condition for calculating a graph's instrinsic complexity by index theorem.
    """

    value: Hashable

    @property
    def nullity(self):
        """
        Returns the dimensionality of the kernel (ie, the number of non-empty origins)
        """
        return len(self.value)

    def __init__(self, *value):
        self.value = frozenset(value)

    def __post_init__(self):
        # sanity check
        assert isinstance(self.value, frozenset)

    def __str__(self):
        return str(self.value)

    __repr__ = __str__

    def __len__(self):
        """
        iNull defines an empty multi-dimensional point. A single point, no matter its dimensionality,
        has measure zero. Otherwise, the object is not a point but rather a distribution.
        """
        return 0

    def __eq__(self, X):
        """
        If both the instance and X have empty values, they share the fundamental
        origin (ie, their "zero" is anonymous in the vein of forgetful functors).
        """
        assert isinstance(X, iNull)
        if self.nullity or X.nullity:
            return (self & X).nullity > 0

        # sanitycheck that both self and X are *empty*
        assert not (self.nullity and X.nullity)
        return True

    def __lt__(self, X):
        assert isinstance(X, iNull)
        return self.nullity < X.nullity

    def __lte__(self, X):
        assert isinstance(X, iNull)
        return self.nullity <= X.nullity

    def __gt__(self, X):
        assert isinstance(X, iNull)
        return self.nullity > X.nullity

    def __gte__(self, X):
        assert isinstance(X, iNull)
        return self.nullity >= X.nullity

    def __or__(self, X):
        assert isinstance(X, iNull)
        return iNull(*self.value.union(X.value))

    def __and__(self, X):
        assert isinstance(X, iNull)
        return iNull(*self.value.intersection(X.value))

    def __xor__(self, X):
        assert isinstance(X, iNull)
        return iNull(*self.value.symmetric_difference(X.value))

    def __iter__(self):
        """
        iNull types represent empty containers and immediately raise a StopIteration
        """
        raise StopIteration(self.__doc__)

    def __bool__(self):
        """
        iNull defines a "boolean zero" like object, so we return False to mimic the
        behavior of 0 and None
        """
        return False

    def __to_json__(self):
        return json.dumps(asdict(self))


class Null(iNull):
    """
    In flow algebra, the null element together with an epsilon neighborhood is enough to reconstruct the kernel and
    therefore the local cohomology for contiguous walks on a directed graph. Different algebras sharing a common origin
    and arithmetical structure are combined by using the null element as an atlas.

    The intuition is the following:

    for $0_n := ker GL[n]$ we have the succession $dim(0_1) < dim(0_2) ... < dim(0_n)$

    The null element is a multiplicative annihilator of the algebraic structure, but furthermore, it is the additive identity
    to the algebra that declares it. This will become a necessary subtly when we switch to cyclic bases.
    """

    # TODO: implement a null element for the cyclic basis
    # TODO: implement descriptor that calculates the index of the epsilon neighborhood as a function of rank and nullity
    atlas = Morphism()  # local coordinate atlas

    @property
    def rank(self):
        """
        Is the dimension of the image of the linear transformation $atlas : V \mapsto W$
        """
        return len(self.atlas.get_kernel(self))

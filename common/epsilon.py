from dataclasses import dataclass, asdict
import json
from .graph import iGraph
from .null import Null
from .category import Morphism
from cytoolz import dicttoolz
from typing import *


@dataclass
class iEpsilon:
    """
    Defines the interface for an epsilon neighborhood, implemented as a descriptor.
    The key functionality is to quickly convert iGraph objects into Epsilon neighborhoods
    """

    # atlas of outgoing vertices
    plus: Morphism
    # atlas of incomming vertices
    minus: Morphism
    # is the base point, or origin, of the topological neighborhood
    null = Null()

    def __get__(self, obj, obj_type=None):
        # return epsilon instance if accessed through the class
        if obj is None:
            return self
        # otherwise, generate an epsilon neighborhood
        return self.from_graph(obj)

    def __set__(self, obj, value):
        """
        Cannot overwrite iEpsilon descriptor
        """
        raise Exception(self.__doc__)

    def __eq__(self, X):
        """
        Compares the values of those keys in the intersection of both epsilons'
        plus and minus dictionaries.
        """
        assert isinstance(X, iEpsilon)
        intersection_p = dicttoolz.keyfilter(lambda x: x in self.plus, X.plus)
        intersection_m = dicttoolz.keyfilter(lambda x: x in self.minus, X.minus)

        # TODO refactor to use either itertoolz or dictoolz to make this c-speed
        for k in intersection_p:
            if self.plus[k] != X.plus[k]:
                return False
        for k in intersection_m:
            if self.minus[k] != X.minus[k]:
                return False

        return self.null == X.null

    def __call__(self, *args):
        """
        Something, something, something dark side. Basically, epsilon is an atlas for a manifold.
        Plus and Minus implement the homomorphism.
        """
        raise NotImplementedError(self.__doc__)

    def __to_iGraph__(self, cast_cls=iGraph):
        """
        Recreates the local graph from the epsilon neighborhoods.
        """

        def outflow():
            return cast_cls(
                (v_src, v_trgt)
                for v_src, target_vs in self.plus.items()
                for v_trgt in target_vs
            )

        def inflow():
            return cast_cls(
                (v_src, v_trgt)
                for v_trgt, source_vs in self.minus.items()
                for v_src in source_vs
            )

        # return the graph union
        return inflow() | outflow()

    def __to_dash__(self):
        """
        TODO: Refactor this functionality out as a mixin class
        """
        return self.factory(self.__to_iGraph__())

    def __to_json__(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_graph(cls, graph: iGraph):
        """
        Factory function to create an epsilon neighborhood from a graph.
        """
        plus = dict()
        minus = dict()
        for e in graph.es:
            tail, head = e.tuple
            plus.setdefault(tail, set()).add(head)
            minus.setdefault(head, set()).add(tail)
        return cls(plus=plus, minus=minus)


@dataclass
class Epsilon(iEpsilon):
    """
    Defines a topological epsilon neighborhood. The intuition is very similar to that
    of conventional topology except that an epsilon neighborhood combines the notion
    of locality with orientation.

    plus := is a dictionary keyed by vertex ID containing the set of outgoing incident vertices
    minus := is a dictionary keyed by vertex ID containing the set of incomming incident vertices
    """

    def __init__(self, plus=None, minus=None):
        plus = plus if plus else dict()
        minus = minus if minus else dict()
        super().__init__(plus=plus, minus=minus)

    @property
    def p(self):
        """
        >>> e = Epsilon(plus={1: {2, 3}}...)
        >>> e.p(1)
        {2, 3}
        """
        return lambda key: self.plus.get(key, self.null)

    @property
    def m(self):
        """
        >>> e = Epsilon(minus={1: {2, 3}}...)
        >>> e.m(1)
        {2, 3}
        """
        return lambda key: self.minus.get(key, self.null)

    def __or__(self, X):
        """
        Joins a pair of epsilons
        """
        plus = dicttoolz.merge(self.plus, X.plus)
        minus = dicttoolz.merge(self.minus, X.minus)
        # null = self.null | X.null
        return Epsilon(plus=plus, minus=minus)

    def __and__(self, X):
        """
        Meets a pair of epsilons
        """
        plus = dicttoolz.merge(self.plus, X.minus)
        minus = dicttoolz.merge(self.minus, X.plus)
        # null = self.null & X.null
        return Epsilon(plus=plus, minus=minus)

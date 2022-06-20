from dataclasses import dataclass
from common.graph import iGraph
from common.epsilon import Epsilon
from common.null import iNull
from cytoolz import itertoolz
from typing import *


@dataclass
class iPath(iGraph):
    """
    Affine Graph:

    A cateory of undirected graphs with graph homomorphisms is projective if the following:

    Let P be a projective graph. For all graphs A, B with surjective homomorphism $s:A \to B$ and
    homomorphism $h: P \to B$, there exists a graph homomorphism $f:P \to A$ such that $h=s \circ f$

    An affine graph category is defined by the collection of morphisms mapping projective graphs P
    to an origin point, the multiplicative annihilator of its path algebra. The functors mapping origin
    to origin form a coordinate atlas.
    """

    epsilon = Epsilon()

    def __init__(self, edges, **kwargs):
        super().__init__(edges, **kwargs)
        for edge in self.es:
            tail, head = edge.tuple
            self.epsilon.plus.setdefault(tail, set()).add(head)
            self.epsilon.minus.setdefault(head, set()).add(tail)


class Path(iPath):
    """
    A path is a subgraph with all vertices of degree 1 or 2 or 3

    TODO: The above is not rigorously true, nor sufficient for the definition of a path.
          This is a poor heuristic definition and the documentation should be rewritten
    """

    @property
    def tail(self):
        """
        First edge of the path
        """
        return itertoolz.first(self.es)

    @property
    def tailv(self):
        """
        Tail of the first edge of the path
        """
        return self.tail.tuple[0]

    @property
    def head(self):
        """
        Last edge of the path
        """
        return itertoolz.last(self.es)

    @property
    def headv(self):
        """
        Head of the last edge of the path
        """
        return self.head.tuple[-1]

    @property
    def tuples(self):
        return tuple(e.tuple for e in self.es)

    def __str__(self):
        return "".join(str(etuple) for etuple in self.tuples)

    def __mul__(self, X):
        """
        Multiplication of paths is concatenation of edges matching head to tail,
        or else "zero" -- ie the empty path.
        """
        if isinstance(X, Path):
            return Path(self.tuples + X.tuples) if self.headv == X.tailv else Path([])
        else:
            # distributivity is as easy as it is hard with duck typing, I leave this for tomorrow
            raise Exception(type(X))

    def __add__(self, X):
        """
        The sum of two paths is an iGraph -- in other words, Path algebras are not
        additively complete (which is why you need flow algebra to begin with)
        """
        return self | X if isinstance(X, Path) else X + self

    def __hash__(self):
        return hash(self.tuples)

    @classmethod
    def factory(cls, *args, **kwargs):
        for arg in args:
            if isinstance(arg, iNull):
                return Path([])
        return cls(args, **kwargs)

    def pushg(self, G):
        """
        Implements the push of a path relative to a graph G
        """
        out_edges = G.vs.find(self.headv).out_edges()
        return iGraph(out_edges)

    def pullg(self, G):
        """
        Implements the pull of a path relative to a graph G
        """
        in_edges = G.vs.find(self.tailv).in_edges()
        return iGraph(in_edges)

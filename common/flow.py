from dataclasses import dataclass, astuple
import json
from .graph import iGraph
from .epsilon import Epsilon
from .path import Path
from itertools import chain, product
from typing import *


@dataclass
class iFlow(set):
    """
    Flow algebras are sets of paths representing morphisms between n-categories of algebraic structures.
    These structures might contain infinitesimals.
    """

    def __init__(self, args, archimedean=True):
        self._archimedean = archimedean  # non-archimedean fields admit infinitesimals
        super().__init__(args if not archimedean else filter(bool, args))

    def __str__(self):
        tostr = lambda element: "(" + ",".join(str(tpl) for tpl in element) + ")"
        return "{" + ", ".join(map(tostr, self)) + "}"

    def __pretty_print__(self):
        tostr = lambda element: "".join(str(tpl) for tpl in element)
        return "+ ".join(map(tostr, self))

    def __add__(self, flow):
        """
        Defaults to the cyclic basis
        """
        # FIXME Flow + Path should be handled as an __radd__ of Path.
        if isinstance(flow, Path):
            return Flow(chain(self, flow), archimedean=self._archimedean)
        return Flow(
            set.symmetric_difference(self, flow),
            archimedean=(self._archimedean or flow._archimedean),
        )

    def __eq__(self, X):
        """
        Defaults to cyclic basis. This the cannonical definition of equality but will not be evident in the
        theory until much later.
        """
        sdiff = self.symmetric_difference(X)
        return True if len(sdiff) == 0 else False

    @property
    def epsilon(self):
        """
        Calculate the epsilon neighborhoods of the flow's paths.
        """
        g = self.__to_iGraph__()
        return Epsilon.from_graph(g)

    @classmethod
    def factory(cls, *args, **kwargs):
        """
        Variadic factory method for creating a Flow.
        """
        return cls(args, **kwargs)

    def __to_dash__(self):
        directed_elements = []
        stylesheet = []
        for path_tuple in self:
            de, ss = Path.factory(path_tuple).__to_dash__()
            directed_elements.extend(de)
            stylesheet.extend(ss)
        return directed_elements, stylesheet

    def __to_json__(self):
        return json.dumps(astuple(self))

    def __to_iGraph__(self):
        return iGraph(chain.from_iterable(self))


class Flow(iFlow):
    """
    A flow is literally a set of paths...with a distributive algebra and maybe infinitesimals
    """

    def __add__(self, flow):
        """
        Defaults to Kleene basis
        """
        if isinstance(flow, Path):
            return Flow(chain(self, flow), archimedean=self._archimedean)
        return Flow(
            set.union(self, flow),
            archimedean=(self._archimedean or flow._archimedean),
        )

    def __mul__(self, flow):
        if isinstance(flow, Path):
            return Flow((Path(p) * flow for p in self), archimedean=self._archimedean)
        archimedean = self._archimedean or flow._archimedean
        distributed = ((Path(px) * Path(py)).tuples for px, py in product(self, flow))
        return Flow(distributed, archimedean=archimedean)

    def pushg(self, graph):
        """
        Outflow
        """
        return Flow(chain.from_iterable(x.pushg(graph) for x in self))

    def pullg(self, graph):
        """
        Inflow
        """
        return Flow(chain.from_iterable(x.pullg(graph) for x in self))

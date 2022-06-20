import json
from igraph import Graph
from itertools import chain, combinations
from typing import *


class iGraph(Graph):
    """
    Interface for graphlike algebraic components that respect local diffeomorphisms
    """

    def __init__(self, edges):
        super().__init__(edges=edges, directed=True)

    @property
    def origin(self):
        """
        Defaults to minimum index of the underlying igraph.Graph. This will break with
        string based indexing (so TBD)
        """
        # FIXME this is extremely brittle and it needs to be made explicit that vertex ids
        #       draw from the pullback of the automorphism group acting on the simple space.
        #       Furthermore, re-using the igraph term of index will be contradictory to our
        #       notion of index (Atiyah & Singer).
        # TODO: implement vertex id as a subclass of uuid with localization conditions (re __eq__)
        return min(v.index for v in self.vs)

    # We should prolly implement these properties and cast to a custom vertex and edge class

    # @property
    # def vs(self):
    #     pass

    # @property
    # def es(self):
    #     pass

    # def __iter__(self):
    #     yield from self.es

    def __contains__(self, key):
        """
        Quickly check whether a vertex, edge, or path is in a graph
        """
        raise NotImplementedError("TBD")

    def __to_dash__(self):
        """
        Quick and dirty parsing for rendering in a Dash app

        TODO: Break this fumctionality out as a mixin class
        """
        nodes = [
            {
                "data": {
                    "id": v.index,
                    "label": v.index,
                    "plus": tuple(s.index for s in v.successors()),
                    "minus": tuple(p.index for p in v.predecessors()),
                }
            }
            for v in self.vs
        ]
        directed_edges = [
            {
                "data": {
                    "id": ",".join(map(str, e.tuple)),
                    "source": e.source,
                    "target": e.target,
                }
            }
            for e in self.es
        ]
        directed_elements = nodes + directed_edges
        node_style = {
            "selector": "node",
            "style": {"background-color": "#BFD7B5", "label": "data(label)"},
        }
        edge_style = {
            "selector": "edge",
            "style": {
                # The default curve style does not work with certain arrows
                "curve-style": "bezier"
            },
        }
        stylesheet = [node_style, edge_style]
        # draw arrows
        for e in self.es:
            style_attributes = {
                "selector": f"#{e.source},{e.target}",
                "style": {
                    "target-arrow-color": "red",
                    "target-arrow-shape": "triangle",
                    "line-color": "green",
                    "mid-source-arrow-shape": "diamond",
                    "mid-source-arrow-fill": "hollow",
                },
            }
            stylesheet.append(style_attributes)
        return directed_elements, stylesheet

    def __to_json__(self):
        return json.dumps(tuple((e.source, e.target) for e in self.es))

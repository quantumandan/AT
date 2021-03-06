Algorithmic Topology
====================

Re-applying the work of Hamilton and Grassmann, with deep inspiration from Lie and Noether and Turing,
a novel enumerative string algebra is defined and couched in the mathematical vernacular of work and 
energy. The action of a Turing machine's successor function is recast in terms of the evolution operator
of a dynamical system, the trajectories of which generate a (data) flow algebra. This representation
provides an unambiguous framework for provably optimal graph traversal; and k-cycle calculation in
**"naively"** polynomial time.

Algorithmic Topology eventually resolves this seeming paradox in the calculation of computational complexity
by representing the execution of an algorithm in terms of its (data)flow, and restricting the configuration
space to those systems which obey conservation of energy.

Flow algebra
------------

It has long been known that given a directed graph $G = (V, E)$, its unweighted adjacency matrix $A$ 
can be used to calculate the number of walks from vertex $V_i$ to vertex $V_j$ of length k. By
theorem, the number of walks of length k from $V_i$ to $V_j$ is given by the $i,j$ th element of $A^k$.

Replacing each "1" in $A$ by the tuple of element coordinates, the resulting array $W$ is the
(unweighted) **walk** matrix of $G$; with addition and multiplication defined as follows:

Addition is the formal sum of objects sharing a category. In the context of flows, or sets of paths, the
formal sum is set inclusion. For $V_i,\space V_j \in V$, the sum of vertices is given by $V_i + V_j:=$ {$V_i,\space V_j$}

Furthermore, with $E_i,\space E_j \in E$ the sum of edges is given by $E_i + E_j:=$ {$E_i,\space E_j$}

The forgetful functor bijectively maps the set of vertices to the integers that label them, allowing the
identification of edges with tuples of integers representing the labels of their constituent verticies. It
follows that the formal sum of edges $E_i = (V_i, V_k)$ and $E_j = (V_j, V_p) \in E$ takes the form,

$(i, k) + (j, p)$ = {$(i, k),\space (j, p)$} for $i, j, k, p \in |V|$

Multiplication is the distributive concatenation of connected edges in E or else "0" (a subtle
but very important point insofar as theory and implementation goes),

$(i, j) \times (j, k)$ := {$(i, j)(j, k)$}

Roughly speaking, "0" refers to the multiplicative sink of the path algebra defined on the
directed graph G. In particular "0" defines the value of,

$(i, j) \times (p, q)$ =  0 if $p \ne j$

An important note is that in addition to being the multiplicative sink, the "0" of a flow algebra must also
be also be the additive identity.

Putting everything together (in a non-rigorous nutshell),

$(a, b) \times ((c, d) + (e, f)) = (a, b) \times (c, d) + (a, b) \times (e, f)$

and for $b = c = e$,

$(a, b) \times ((b, d) + (b, f)) =$ {$(a, b)(b, d),\space (a, b)(b, f)$}

The graph generating this idiotically simple algebra, by replacing numbers with shapes, is identified with
a simplicial complex.

Pulling a rabbit out of a hats
------------------------------

The fundamental intuition is that every algebra of symbols is the generator for a bialgebraic structure
generated by containers holding a single symbol. The key insight is that while these container algebras satisfy
identical rules of arithmetic, their capacity to carry information is significantly larger. This is why
there exists a *polynomially expressible* formula for an NP-Hard problem that has no P implementation.

Summary
-------

Algorithmic Topology is the field of study that quantifies, investigates, and eventually resolves
a seeming paradox in the calculation of computational complexity by representing the execution of
an algorithm in terms of its data flow.

* A Vertex is a size 1 tuple (0-simplex)
* An Edge is a size 2 tuple of verticies (1-simplex)
* An n-Path is a size n tuple of n-edges sequentially connected head to tail
* A rank n Flow is a set of k-paths for k < n
* A Graph $G = (V, E)$ is completely determined by the adjacency bijection $(V, E) \mapsto A$
* The unweighted adjacency matrix $A$ is a key topological invariant, and generates the walk matrix $W$

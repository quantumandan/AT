Flow Algebra
============

It has long been known that given a directed graph $G = (V, E)$, its unweighted adjacency matrix $A$ 
can be used to calculate the number of walks from vertex $V_i$ to vertex $V_j$ of length k. By
theorem, the number of walks of length k from $V_i$ to $V_j$ is given by the $(i, j)$th element of $A^k$.

Replacing each "1" in $A$ by the tuple of element coordinates, the resulting array $W$ is the
(unweighted) **walk** matrix of $G$; with addition and multiplication defined as follows:

Addition is the formal sum of objects sharing a category. In the context of flows, or sets of paths, the
formal sum is set inclusion. For $V_i, V_j \in V$, the sum of vertices is given by $V_i+V_j:=\{V_i, V_j\}$

Furthermore, with $E_i, E_j \in E$ the sum of edges is given by $E_i + E_j:=\{E_i, E_j\}$

The forgetful functor bijectively maps the set of vertices to the integers that label them, allowing the
identification of edges with tuples of integers representing the labels of their constituent verticies. It
follows that the formal sum of edges $E_i = (V_i, V_k), E_j = (V_j, V_p) \in E$ takes the form,

(i, k) + (j, p) = {(i, k), (j, p)} for i, j, k, p in $\abs(V)$

Multiplication is the distributive concatenation of connected edges in E or else "0" (a subtle
but very important point insofar as theory and implementation goes),

(i, j) x (j, k) := {(i, j)(j, k)}

Roughly speaking, "0" refers to the multiplicative sink of the path algebra defined on the
directed graph G. In particular "0" defines the value of,

(i, j) x (p, q) =  0 if p != j

Putting everything together (in a non-rigorous nutshell),

(a, b) x ( (c, d) + (e, f) ) = (a, b) x (c, d) + (a, b) x (e, f),

and for b == c == e,

(a, b) x ( (b, d) + (b, f) ) = {(a, b)(b, d), (a, b)(b, f)}

Re-applying the work of Hamilton and Grassmann, we define a novel enumerative string algebra and 
couch it in over a hundred years of well explored mathematical physics. Reappropriating the
mathematical vernacular of work and energy, the operation of a Turing machine is recast as in terms
of the evolution operator of a dynamical system, the output of which generates the (data) flow algebra.
This representation provides an unambiguous framework for provably optimal graph traversal; and
Hamiltonian cycle calculation in **"naively"** polynomial time.

After much study, this idiotically simple algebra is proved to be indistiguishably isomorphic to
the algebra of exact differential forms.

Algorithmic Topology is the field of study that quantifies, investigates, and eventually resolves
this seeming paradox in the calculation of computational complexity by representing the execution of
an algorithm in terms of its (data)flow.

A Vertex is a size 1 tuple
An Edge is a size 2 tuple of verticies
An n-Path is a size n tuple of n-edges sequentially connected head to tail
A rank n Flow is a set of k-paths for k < n
A blade of epsilons directed graph
A Graph G = (V, E) is completely determined by the adjacency bijection (V, E) \mapsto A
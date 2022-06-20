import unittest
from common.graph import iGraph
from common.epsilon import Epsilon
from common.null import iNull
from vuln import Path, Flow
from igraph import Graph
from cytoolz import dicttoolz
from itertools import chain


class CommonTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.intv = list(range(200))
        self.strv = list(map(str, self.intv))
        for i in self.intv:
            for j in self.intv:
                setattr(self, f"e{i}{j}_intv", (i, j))
                setattr(self, f"e{i}{j}_strv", (self.strv[i], self.strv[j]))
        return super().setUp()


class TestNull(unittest.TestCase):
    def test_empty_null_from_init(self):
        null = iNull()
        self.assertIsInstance(null, iNull)
        self.assertIsInstance(null.value, frozenset)

    def test_trivial_non_empty_null_from_init(self):
        null = iNull(0)
        self.assertIsInstance(null, iNull)
        self.assertIsInstance(null.value, frozenset)
        self.assertSetEqual(null.value, frozenset([0]))

    def test_non_trivial_non_empty_null_from_init(self):
        null = iNull(0, 1, 2)
        self.assertIsInstance(null, iNull)
        self.assertIsInstance(null.value, frozenset)
        self.assertSetEqual(null.value, frozenset([0, 1, 2]))

    def test_trivial_empty_nulls_join(self):
        null_1 = iNull()
        null_2 = iNull()
        joined_null = null_1 | null_2
        self.assertIsInstance(joined_null, iNull)
        self.assertIsInstance(joined_null.value, frozenset)
        self.assertSetEqual(joined_null.value, frozenset())

    def test_trivial_non_empty_nulls_join(self):
        # test left join
        null_1 = iNull(0)
        null_2 = iNull()
        joined_null = null_1 | null_2
        self.assertIsInstance(joined_null, iNull)
        self.assertIsInstance(joined_null.value, frozenset)
        self.assertSetEqual(joined_null.value, frozenset([0]))

        # test right join
        null_1 = iNull()
        null_2 = iNull(0)
        joined_null = null_1 | null_2
        self.assertIsInstance(joined_null, iNull)
        self.assertIsInstance(joined_null.value, frozenset)
        self.assertSetEqual(joined_null.value, frozenset([0]))

    def test_non_empty_nulls_join_disjoint(self):
        null_1 = iNull(0, 1, 2)
        null_2 = iNull(3)
        joined_null = null_1 | null_2
        self.assertIsInstance(joined_null, iNull)
        self.assertIsInstance(joined_null.value, frozenset)
        self.assertSetEqual(joined_null.value, frozenset([0, 1, 2, 3]))

    def test_non_empty_nulls_join_not_disjoint(self):
        null_1 = iNull(0, 1, 2)
        null_2 = iNull(0, 3)
        joined_null = null_1 | null_2
        self.assertIsInstance(joined_null, iNull)
        self.assertIsInstance(joined_null.value, frozenset)
        self.assertSetEqual(joined_null.value, frozenset([0, 1, 2, 3]))

    def test_trivial_empty_nulls_meet(self):
        null_1 = iNull()
        null_2 = iNull()
        meeted_null = null_1 & null_2
        self.assertIsInstance(meeted_null, iNull)
        self.assertIsInstance(meeted_null.value, frozenset)
        self.assertSetEqual(meeted_null.value, frozenset())

    def test_trivial_non_empty_nulls_meet(self):
        # test left meet
        null_1 = iNull(0)
        null_2 = iNull()
        meeted_null = null_1 & null_2
        self.assertIsInstance(meeted_null, iNull)
        self.assertIsInstance(meeted_null.value, frozenset)
        self.assertSetEqual(meeted_null.value, frozenset())

        # test right meet
        null_1 = iNull()
        null_2 = iNull(0)
        meeted_null = null_1 | null_2
        self.assertIsInstance(meeted_null, iNull)
        self.assertIsInstance(meeted_null.value, frozenset)
        self.assertSetEqual(meeted_null.value, frozenset([0]))

    def test_non_empty_nulls_meet_disjoint(self):
        null_1 = iNull(0, 1, 2)
        null_2 = iNull(3)
        meeted_null = null_1 & null_2
        self.assertIsInstance(meeted_null, iNull)
        self.assertIsInstance(meeted_null.value, frozenset)
        self.assertSetEqual(meeted_null.value, frozenset())

    def test_non_empty_nulls_meet_not_disjoint(self):
        null_1 = iNull(0, 1, 2, 3)
        null_2 = iNull(0, 3)
        meeted_null = null_1 & null_2
        self.assertIsInstance(meeted_null, iNull)
        self.assertIsInstance(meeted_null.value, frozenset)
        self.assertSetEqual(meeted_null.value, frozenset([0, 3]))


class TestEpsilon(CommonTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.g = Graph.Full(int(len(self.intv) / 2))
        self.g.vs["name"] = self.strv
        self.g.es["name"] = list("".join(str(_) for _ in e.tuple) for e in self.g.es)

    def test_vertex_epsilon(self):
        # create single epsilon
        plus0 = {0: set([1])}
        minus0 = {1: set([0])}
        e_v0 = Epsilon(plus=plus0, minus=minus0)
        self.assertEqual(e_v0, e_v0)

        plus1 = {1: set([2]), 2: set([3]), 3: set([1])}
        minus1 = {1: set([0, 3]), 2: set([1]), 3: set([2])}
        e_v1 = Epsilon(plus=plus1, minus=minus1)
        self.assertEqual(e_v1, e_v1)

        self.assertFalse(e_v0 == e_v1)

    def test_vertex_epsilon_meet(self):
        plus0 = {0: set([1])}
        minus0 = {1: set([0])}
        e_v0 = Epsilon(plus=plus0, minus=minus0)

        plus1 = {1: set([2]), 2: set([3]), 3: set([1])}
        minus1 = {1: set([0, 3]), 2: set([1]), 3: set([2])}
        e_v1 = Epsilon(plus=plus1, minus=minus1)

        plus3 = dicttoolz.merge(plus0, minus1)
        minus3 = dicttoolz.merge(minus0, plus1)

        meeted = e_v0 & e_v1
        expected_value = Epsilon(plus=plus3, minus=minus3)

        self.assertDictEqual(meeted.plus, expected_value.plus)
        self.assertDictEqual(meeted.minus, expected_value.minus)
        self.assertEqual(meeted, expected_value)

    def test_vertex_epsilon_join(self):
        plus0 = {0: set([1])}
        minus0 = {1: set([0])}
        e_v0 = Epsilon(plus=plus0, minus=minus0)

        plus1 = {1: set([2]), 2: set([3]), 3: set([1])}
        minus1 = {1: set([0, 3]), 2: set([1]), 3: set([2])}
        e_v1 = Epsilon(plus=plus1, minus=minus1)

        plus3 = dicttoolz.merge(plus0, plus1)
        minus3 = dicttoolz.merge(minus0, minus1)

        joined = e_v0 | e_v1
        expected_value = Epsilon(plus=plus3, minus=minus3)

        self.assertDictEqual(joined.plus, expected_value.plus)
        self.assertDictEqual(joined.minus, expected_value.minus)
        self.assertEqual(joined, expected_value)

    def test_epsilon_factory(self):
        g = iGraph(e.tuple for e in self.g.es)
        epsilon = Epsilon.from_graph(g)
        for e in self.g.es:
            tail, head = e.tuple
            self.assertTrue(head in epsilon.p(tail))
            self.assertTrue(tail in epsilon.m(head))

    # def test_epsilon_factory_on_path(self):
    #     epsilon = Epsilon.factory(self.g)


# class TestVertex(unittest.TestCase):
#     pass

# class TestEdge(unittest.TestCase):
#     pass


class TestPath(CommonTestCase):
    def test_init_Path_factory_intv_single_element(self):
        p_intv = Path.factory(self.e12_intv)
        self.assertEqual(p_intv.tuples, (self.e12_intv,))

    def test_init_Path_factory_intv_two_elements(self):
        p_intv = Path.factory(self.e12_intv, self.e23_intv)
        self.assertEqual(p_intv.tuples, (self.e12_intv, self.e23_intv))

    def test_init_Path_factory_intv_inductive(self):
        p_intv = Path.factory(self.e12_intv, self.e23_intv, self.e34_intv)
        self.assertEqual(p_intv.tuples, (self.e12_intv, self.e23_intv, self.e34_intv))

    # def test_init_factory_strv_single_element(self):
    #     p_strv = Path.factory(("1", "2"))

    # def test_init_factory_strv_two_elements(self):
    #     p_strv = Path.factory(("1", "2"), ("2", "3"))

    # def test_init_factory_strv_inductive(self):
    #     p_strv = Path.factory(("1", "2"), ("2", "3"))

    def test_add_intv_paths(self):
        p1_intv = Path.factory(self.e12_intv)
        p2_intv = Path.factory(self.e23_intv)
        p_sum = p1_intv + p2_intv
        self.assertTrue(issubclass((p1_intv + p2_intv).__class__, set))
        self.assertEqual(p1_intv + p2_intv, set(((1, 2), (2, 3))))

    def test_multiply_intv_two_paths_matching_head_to_tail(self):
        p1_intv = Path.factory(self.e12_intv)
        p2_intv = Path.factory(self.e23_intv)
        self.assertEqual(
            (p1_intv * p2_intv).tuples,
            Path.factory(self.e12_intv, self.e23_intv).tuples,
        )

    def test_multiply_intv_three_paths_matching_head_to_tail(self):
        p1_intv = Path.factory(self.e12_intv)
        p2_intv = Path.factory(self.e23_intv)
        p3_intv = Path.factory(self.e34_intv)
        self.assertEqual(
            (p1_intv * p2_intv * p3_intv).tuples,
            Path.factory(self.e12_intv, self.e23_intv, self.e34_intv).tuples,
        )

    def test_multiply_intv_inductive_paths_matching_head_to_tail(self):
        p1_intv = Path.factory(self.e12_intv)
        p2_intv = Path.factory(self.e23_intv)
        p3_intv = Path.factory(self.e34_intv)
        p4_intv = Path.factory(self.e45_intv)
        self.assertEqual(
            (p1_intv * p2_intv * p3_intv * p4_intv).tuples,
            Path.factory(
                self.e12_intv, self.e23_intv, self.e34_intv, self.e45_intv
            ).tuples,
        )

    def test_multiply_intv_trivial_paths_not_matching_head_to_tail(self):
        p1_intv = Path.factory(self.e12_intv)
        p2_intv = Path.factory(self.e23_intv)
        assert p1_intv.epsilon.null == p2_intv.epsilon.null
        pprod = p2_intv * p1_intv
        self.assertEqual(pprod, Path([]))

    def test_multiply_intv_complex_paths_not_matching_head_to_tail(self):
        p123_intv = Path.factory(self.e12_intv, self.e23_intv)
        p23_intv = Path.factory(self.e23_intv)
        p234_intv = Path.factory(self.e23_intv, self.e34_intv)
        p4567_intv = Path.factory(self.e45_intv, self.e56_intv, self.e67_intv)

        assert p123_intv.epsilon.null == p23_intv.epsilon.null
        pprod = p123_intv * p23_intv
        self.assertEqual(pprod, Path([]))

        assert p234_intv.epsilon.null == p23_intv.epsilon.null
        pprod = p23_intv * p234_intv
        self.assertEqual(pprod, Path([]))

        assert p123_intv.epsilon.null == p4567_intv.epsilon.null
        pprod = p123_intv * p4567_intv
        self.assertEqual(pprod, Path([]))

    def test_path_times_flow_is_subclass_of_flow(self):
        p_intv1 = Path.factory(self.e12_intv)
        p_intv2 = Path.factory(self.e23_intv)
        p_intv3 = Path.factory(self.e32_intv)
        flow = Flow.factory(p_intv1, p_intv2)
        product_flow = p_intv3 * flow
        self.assterTrue(isinstance(product_flow, Flow))


class TestFlow(CommonTestCase):
    def test_Flow_dunder_equality_with_set(self):
        f_intv = Flow([self.e12_intv])
        self.assertEqual(f_intv, set([self.e12_intv]))

    def test_flow_dunder_iter(self):
        f_intv = Flow.factory((self.e12_intv, self.e23_intv), self.e34_intv)
        self.assertEqual(
            set([(self.e12_intv, self.e23_intv), self.e34_intv]), set(list(f_intv))
        )

    def test_init_Flow_factory_intv_single_element(self):
        f_intv = Flow.factory(self.e12_intv)
        expected = Flow([self.e12_intv])
        self.assertEqual(f_intv, expected)

    def test_init_Flow_factory_intv_two_elements(self):
        f_intv = Flow.factory(self.e12_intv, self.e23_intv)
        self.assertEqual(
            f_intv,
            set(
                (self.e12_intv, self.e23_intv),
            ),
        )

    def test_init_Flow_factory_intv_inductive(self):
        f_intv = Flow.factory((self.e12_intv, self.e23_intv), self.e34_intv)
        self.assertEqual(f_intv, set([(self.e12_intv, self.e23_intv), self.e34_intv]))

    # def test_init_factory_strv_single_element(self):
    #     p_strv = Path.factory(("1", "2"))

    # def test_init_factory_strv_two_elements(self):
    #     p_strv = Path.factory(("1", "2"), ("2", "3"))

    # def test_init_factory_strv_inductive(self):
    #     p_strv = Path.factory(("1", "2"), ("2", "3"))

    def test_add_flows_returns_flow(self):
        f_intv1 = Flow.factory(self.e12_intv)
        f_intv2 = Flow.factory(self.e23_intv)
        f_sum12 = f_intv1 + f_intv2
        self.assertTrue(isinstance(f_sum12, Flow))

    def test_add_flow_with_null_path_to_flow_with_null_path_returns_flow(self):
        f_intv_empty1 = Flow.factory(Path([]))
        f_intv_empty2 = Flow.factory(Path([]))
        f_sum = f_intv_empty1 + f_intv_empty2
        self.assertTrue(isinstance(f_sum, Flow))
        self.assertEqual(f_sum, Flow.factory(Path([])))

    def test_add_archimedean_flow_with_null_path_to_flow_returns_flow(self):
        f_intv = Flow.factory(self.e12_intv)
        f_intv_empty = Flow.factory(Path([]))
        f_sum = f_intv + f_intv_empty
        self.assertTrue(isinstance(f_sum, Flow))
        self.assertEqual(f_sum, f_intv)

    def test_add_non_archimedean_flow_with_null_path_to_flow_returns_flow(self):
        f_intv = Flow.factory(self.e12_intv, archimedean=False)
        f_intv_empty = Flow.factory(Path([]), archimedean=False)
        f_sum = f_intv + f_intv_empty
        self.assertTrue(isinstance(f_sum, Flow))
        self.assertNotEqual(f_sum, f_intv)

    def test_add_two_trivial_intv_flows(self):
        f_intv1 = Flow.factory(self.e12_intv)
        f_intv2 = Flow.factory(self.e23_intv)
        f_sum12 = f_intv1 + f_intv2
        self.assertEqual(f_sum12, Flow.factory(self.e12_intv, self.e23_intv))

    def test_add_three_trivial_intv_flows(self):
        f_intv1 = Flow.factory(self.e12_intv)
        f_intv2 = Flow.factory(self.e23_intv)
        f_intv3 = Flow.factory(self.e34_intv)
        f_sum123 = f_intv1 + f_intv2 + f_intv3
        self.assertEqual(
            f_sum123, Flow.factory(self.e12_intv, self.e23_intv, self.e34_intv)
        )

    def test_add_two_intv_flows_different_path_sizes(self):
        p123 = Path.factory(self.e12_intv, self.e23_intv, self.e34_intv)
        p45 = Path.factory(self.e45_intv, self.e56_intv)
        f_intv1 = Flow.factory(p123.tuples)
        f_intv2 = Flow.factory(p45.tuples)
        f_sum123 = f_intv1 + f_intv2
        self.assertEqual(f_sum123, Flow.factory(p123.tuples, p45.tuples))
        self.assertEqual(
            f_sum123.epsilon, Epsilon.from_graph(iGraph(chain(p123.tuples, p45.tuples)))
        )

    def test_add_intv_two_identical_flows(self):
        f_intv = Flow.factory(self.e12_intv)
        self.assertEqual(f_intv + f_intv, f_intv)

    # def test_multiply_intv_three_paths_matching_head_to_tail(self):
    #     p_intv1 = Path.factory(self.e12_intv)
    #     p_intv2 = Path.factory(self.e23_intv)
    #     p_intv3 = Path.factory(self.e34_intv)
    #     self.assertEqual(
    #         (p_intv1 * p_intv2 * p_intv3).tuples,
    #         Path.factory(self.e12_intv, self.e23_intv, self.e34_intv).tuples,
    #     )

    # def test_multiply_intv_inductive_paths_matching_head_to_tail(self):
    #     p_intv1 = Path.factory((1, 2))
    #     p_intv2 = Path.factory((2, 3))
    #     p_intv3 = Path.factory((3, 4))
    #     p_intv3 = Path.factory((4, 5))
    #     self.assertEqual(
    #         (p_intv1 * p_intv2 * p_intv3).tuples,
    #         Path.factory((1, 2), (2, 3), (3, 4), (4, 5)).tuples,
    #     )

    # def test_multiply_intv_paths_not_matching_head_to_tail(self):
    #     p_intv1 = Path.factory((1, 2))
    #     p_intv2 = Path.factory((2, 3))
    #     self.assertEqual(p_intv2 * p_intv1, Path.factory((1, 2), (2, 3)).epsilon.null)

    def test_flow_distributivity_simple(self):
        p_intv1 = Path.factory(self.e12_intv)
        p_intv2 = Path.factory(self.e23_intv)
        p_intv3 = Path.factory(self.e32_intv)
        summed = p_intv2 + p_intv3
        expected = p_intv1 * p_intv2 + p_intv1 * p_intv3
        distributed = p_intv1 * summed
        self.assertEqual(distributed, expected)

    # def test_path_times_flow_is_flow_with_distributivity(self):
    #     p_intv1 = Path.factory(self.e12_intv)
    #     p_intv2 = Path.factory(self.e23_intv)
    #     p_intv3 = Path.factory(self.e32_intv)
    #     flow = p_intv1 + p_intv2
    #     expected_product = Flow.factory((p_intv3 * p_intv2).tuples)
    #     actual_product = Flow.factory(p_intv3) * flow
    #     self.assertEqual(actual_product, expected_product)

    def test_push_simple_flow(self):
        pass

    def test_pull_simple_flow(self):
        pass


class TestGraph(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()

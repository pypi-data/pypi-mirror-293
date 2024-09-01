import pytest

from minedag import MineDag


@pytest.fixture(scope='function')
def dag_1():
    r"""
        1      9     11   12         13
       / \     |              w2->  /  \  <- w3
      2   3    10                  14   15
w3->  | / |
      4   | <- w5
w2->  | \ |
      5   6
      \  /
       7
       |
       8
    """
    dag = MineDag()
    dag.add_edge(1, 2)
    dag.add_edge(1, 3)
    dag.add_edge(2, 4, weight=3)
    dag.add_edge(3, 4)
    dag.add_edge(4, 5, weight=2)
    dag.add_edge(3, 6, weight=5)
    dag.add_edge(4, 6)
    dag.add_edge(5, 7)
    dag.add_edge(6, 7)
    dag.add_edge(7, 8)
    dag.add_edge(9, 10)

    dag.add_edge(13, 14, weight=2)
    dag.add_edge(13, 15, weight=3)

    dag.add_node(11)
    dag.add_node(12)
    return dag


def test_get_all_roots(dag_1):
    assert dag_1.get_all_roots() == {1, 9, 11, 12, 13}


def test_get_leaves(dag_1):
    assert dag_1.get_leaves() == {8, 10, 11, 12, 14, 15}


def test_get_all_srcs(dag_1):
    assert dag_1.get_all_srcs(1) == []
    assert dag_1.get_all_srcs(2) == [1]
    assert dag_1.get_all_srcs(3) == [1]
    assert dag_1.get_all_srcs(4) in [[2, 3, 1], [3, 2, 1]]
    assert dag_1.get_all_srcs(5) in [[4, 2, 3, 1], [4, 3, 2, 1]]
    assert dag_1.get_all_srcs(6) in [[4, 2, 3, 1], [4, 3, 2, 1], [3, 4, 2, 1]]
    assert dag_1.get_all_srcs(7) in [[5, 6, 4, 2, 3, 1], [6, 5, 4, 2, 3, 1], [5, 6, 4, 3, 2, 1], [6, 5, 4, 3, 2, 1]]
    assert dag_1.get_all_srcs(8) in [[7, 5, 6, 4, 2, 3, 1], [7, 6, 5, 4, 2, 3, 1], [7, 5, 6, 4, 3, 2, 1], [7, 6, 5, 4, 3, 2, 1]]
    assert dag_1.get_all_srcs(9) == []
    assert dag_1.get_all_srcs(10) == [9]
    assert dag_1.get_all_srcs(11) == []
    assert dag_1.get_all_srcs(12) == []
    assert dag_1.get_all_srcs(13) == []
    assert dag_1.get_all_srcs(14) == [13]
    assert dag_1.get_all_srcs(15) == [13]


def test_get_all_depencies(dag_1):
    assert dag_1.get_all_dsts(1) in [
        [2, 3, 4, 5, 6, 7, 8],
        [2, 3, 4, 6, 5, 7, 8],
        [3, 2, 4, 5, 6, 7, 8],
        [3, 2, 4, 6, 5, 7, 8],
    ]
    assert dag_1.get_all_dsts(2) in [[4, 5, 6, 7, 8], [4, 6, 5, 7, 8]]
    assert dag_1.get_all_dsts(3) in [[4, 5, 6, 7, 8], [4, 6, 5, 7, 8]]
    assert dag_1.get_all_dsts(4) in [[5, 6, 7, 8], [6, 5, 7, 8]]
    assert dag_1.get_all_dsts(5) == [7, 8]
    assert dag_1.get_all_dsts(6) == [7, 8]
    assert dag_1.get_all_dsts(7) == [8]
    assert dag_1.get_all_dsts(8) == []
    assert dag_1.get_all_dsts(9) == [10]
    assert dag_1.get_all_dsts(10) == []
    assert dag_1.get_all_dsts(11) == []
    assert dag_1.get_all_dsts(12) == []
    assert dag_1.get_all_dsts(13) in [[14, 15], [15, 14]]
    assert dag_1.get_all_dsts(14) == []
    assert dag_1.get_all_dsts(15) == []


def test_find_shortest_way_to_any_leaf(dag_1):
    assert dag_1.find_shortest_way_to_any_leaf(1) == (5, [3, 4, 6, 7, 8])
    assert dag_1.find_shortest_way_to_any_leaf(2) == (4, [4, 6, 7, 8])
    assert dag_1.find_shortest_way_to_any_leaf(3) == (4, [4, 6, 7, 8])
    assert dag_1.find_shortest_way_to_any_leaf(4) == (3, [6, 7, 8])
    assert dag_1.find_shortest_way_to_any_leaf(5) == (2, [7, 8])
    assert dag_1.find_shortest_way_to_any_leaf(6) == (2, [7, 8])
    assert dag_1.find_shortest_way_to_any_leaf(7) == (1, [8])
    assert dag_1.find_shortest_way_to_any_leaf(8) == (0, [])
    assert dag_1.find_shortest_way_to_any_leaf(9) == (1, [10])
    assert dag_1.find_shortest_way_to_any_leaf(10) == (0, [])
    assert dag_1.find_shortest_way_to_any_leaf(11) == (0, [])
    assert dag_1.find_shortest_way_to_any_leaf(12) == (0, [])
    assert dag_1.find_shortest_way_to_any_leaf(13) == (2, [14])
    assert dag_1.find_shortest_way_to_any_leaf(14) == (0, [])
    assert dag_1.find_shortest_way_to_any_leaf(15) == (0, [])


def test_find_shortest_way_to_farthest_leaf(dag_1):
    assert dag_1.find_shortest_way_to_farthest_leaf(1) == (5, [3, 4, 6, 7, 8])
    assert dag_1.find_shortest_way_to_farthest_leaf(2) == (4, [4, 6, 7, 8])
    assert dag_1.find_shortest_way_to_farthest_leaf(3) == (4, [4, 6, 7, 8])
    assert dag_1.find_shortest_way_to_farthest_leaf(4) == (3, [6, 7, 8])
    assert dag_1.find_shortest_way_to_farthest_leaf(5) == (2, [7, 8])
    assert dag_1.find_shortest_way_to_farthest_leaf(6) == (2, [7, 8])
    assert dag_1.find_shortest_way_to_farthest_leaf(7) == (1, [8])
    assert dag_1.find_shortest_way_to_farthest_leaf(8) == (0, [])
    assert dag_1.find_shortest_way_to_farthest_leaf(9) == (1, [10])
    assert dag_1.find_shortest_way_to_farthest_leaf(10) == (0, [])
    assert dag_1.find_shortest_way_to_farthest_leaf(11) == (0, [])
    assert dag_1.find_shortest_way_to_farthest_leaf(12) == (0, [])
    assert dag_1.find_shortest_way_to_farthest_leaf(13) == (3, [15])
    assert dag_1.find_shortest_way_to_farthest_leaf(14) == (0, [])
    assert dag_1.find_shortest_way_to_farthest_leaf(15) == (0, [])


def test_find_longest_way_to_any_leaf(dag_1):
    assert dag_1.find_longest_way_to_any_leaf(1) == (8, [2, 4, 5, 7, 8])
    assert dag_1.find_longest_way_to_any_leaf(2) == (7, [4, 5, 7, 8])
    assert dag_1.find_longest_way_to_any_leaf(3) == (7, [4, 5, 7, 8])
    assert dag_1.find_longest_way_to_any_leaf(4) == (7, [6, 7, 8])
    assert dag_1.find_longest_way_to_any_leaf(5) == (2, [7, 8])
    assert dag_1.find_longest_way_to_any_leaf(6) == (2, [7, 8])
    assert dag_1.find_longest_way_to_any_leaf(7) == (1, [8])
    assert dag_1.find_longest_way_to_any_leaf(8) == (0, [])
    assert dag_1.find_longest_way_to_any_leaf(9) == (1, [10])
    assert dag_1.find_longest_way_to_any_leaf(10) == (0, [])
    assert dag_1.find_longest_way_to_any_leaf(11) == (0, [])
    assert dag_1.find_longest_way_to_any_leaf(12) == (0, [])
    assert dag_1.find_longest_way_to_any_leaf(13) == (3, [15])
    assert dag_1.find_longest_way_to_any_leaf(14) == (0, [])
    assert dag_1.find_longest_way_to_any_leaf(15) == (0, [])


def test_find_longest_way_to_farthest_leaf(dag_1):
    assert dag_1.find_longest_way_to_farthest_leaf(1) == (8, [2, 4, 5, 7, 8])
    assert dag_1.find_longest_way_to_farthest_leaf(2) == (7, [4, 5, 7, 8])
    assert dag_1.find_longest_way_to_farthest_leaf(3) == (7, [4, 5, 7, 8])
    assert dag_1.find_longest_way_to_farthest_leaf(4) == (7, [6, 7, 8])
    assert dag_1.find_longest_way_to_farthest_leaf(5) == (2, [7, 8])
    assert dag_1.find_longest_way_to_farthest_leaf(6) == (2, [7, 8])
    assert dag_1.find_longest_way_to_farthest_leaf(7) == (1, [8])
    assert dag_1.find_longest_way_to_farthest_leaf(8) == (0, [])
    assert dag_1.find_longest_way_to_farthest_leaf(9) == (1, [10])
    assert dag_1.find_longest_way_to_farthest_leaf(10) == (0, [])
    assert dag_1.find_longest_way_to_farthest_leaf(11) == (0, [])
    assert dag_1.find_longest_way_to_farthest_leaf(12) == (0, [])
    assert dag_1.find_longest_way_to_farthest_leaf(13) == (3, [15])
    assert dag_1.find_longest_way_to_farthest_leaf(14) == (0, [])
    assert dag_1.find_longest_way_to_farthest_leaf(15) == (0, [])

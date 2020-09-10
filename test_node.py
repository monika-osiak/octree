import pytest
from models import Node
from functions import get_grid, print_preorder


class TestNode:
    def test_create_root(self):
        root = Node(
            [0, 0, 0],
            [1, 2, 3]
        )
        assert root.x == 0
        assert root.y == 0
        assert root.z == 0
        assert root.dx == 1
        assert root.dy == 2
        assert root.dz == 3
        assert root.is_leaf is True

    def test_create_children(self):
        root = Node(
            [0, 0, 0],
            [1, 2, 3]
        )
        root.split()
        assert root.is_leaf is False
        for child in root.branches:
            assert child is not None

    def test_second_level(self):
        root = Node(
            [0, 0, 0],
            [1, 2, 3]
        )
        root.split()

        last_child = root.branches[0b111]
        assert last_child.x == 0.5
        assert last_child.y == 1
        assert last_child.z == 1.5
        assert last_child.dx == 0.5
        assert last_child.dy == 1
        assert last_child.dz == 1.5

    def test_third_level(self):
        root = Node(
            [0, 0, 0],
            [1, 2, 3]
        )
        root.split()
        last_child = root.branches[0b111]
        last_child.split()
        some_child = last_child.branches[0b110]
        assert some_child.x == 0.5
        assert some_child.y == 1.5
        assert some_child.z == 2.25
        assert some_child.dx == 0.25
        assert some_child.dy == 0.5
        assert some_child.dz == 0.75

    def test_get_grid(self):
        root = Node(
            [0, 0, 0],
            [1, 2, 3]
        )
        get_grid(root, condition=0.2)
        print_preorder(root)

        assert root.is_leaf is False

        second_level = root.branches[1]
        assert second_level.is_leaf is False

        third_level = second_level.branches[1]
        assert third_level.is_leaf is False

        fourth_level = third_level.branches[1]
        assert fourth_level.is_leaf is True
        assert fourth_level.dx == 0.125
        assert fourth_level.dy == 0.250
        assert fourth_level.dz == 0.375

    def test_get_point(self):
        root = Node(
            [0, 0, 0],
            [10, 10, 10]
        )
        get_grid(root, condition=3)
        point_to_check = [7, 7, 7]
        node = root.find_point(point_to_check)
        assert node.x == 5
        assert node.y == 5
        assert node.z == 5
        assert node.dx == 2.5
        assert node.dy == 2.5
        assert node.dz == 2.5

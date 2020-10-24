import pytest
from models import Node, Point, Vector
from functions import get_grid, print_preorder


class TestOctree:
    def test_create_root(self):
        root = Node(
            Point(0, 0, 0),
            Vector(1, 2, 3)
        )
        assert root.start == Point(0, 0, 0)
        assert len(root.edges) == 12
        assert len(root.walls) == 6
        assert root.is_leaf is True

    def test_create_children(self):
        root = Node(
            Point(0, 0, 0),
            Vector(1, 2, 3)
        )
        root.split()
        assert root.is_leaf is False
        for child in root.branches:
            assert child is not None

    def test_second_level(self):
        root = Node(
            Point(0, 0, 0),
            Vector(1, 2, 3)
        )
        root.split()

        last_child = root.branches[0b111]
        assert last_child.start == Point(0.5, 1, 1.5)
        assert last_child.dim == Vector(0.5, 1, 1.5)

    def test_third_level(self):
        root = Node(
            Point(0, 0, 0),
            Vector(1, 2, 3)
        )
        root.split()
        last_child = root.branches[0b111]
        last_child.split()
        some_child = last_child.branches[0b110]

        assert some_child.start == Point(0.5, 1.5, 2.25)
        assert some_child.dim == Vector(0.25, 0.5, 0.75)

    def test_get_grid(self):
        root = Node(
            Point(0, 0, 0),
            Vector(1, 2, 3)
        )
        get_grid(root, condition=0.07)
        print_preorder(root)

        assert root.is_leaf is False

        second_level = root.branches[1]
        assert second_level.is_leaf is False

        third_level = second_level.branches[1]
        assert third_level.is_leaf is True
        assert third_level.dim == Vector(0.25, 0.5, 1)

    def test_get_point(self):
        root = Node(
            Point(0, 0, 0),
            Vector(1, 2, 3)
        )
        get_grid(root, condition=3)
        point_to_check = Point(7, 7, 7)
        node = root.find_point(point_to_check)

        assert node.start == Point(5, 5, 5)
        assert node.dim == Vector(2.5, 2.5, 2.5)

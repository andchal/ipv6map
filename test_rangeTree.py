from unittest import TestCase
from rangetree import Point, RangeTree, BBox
from itertools import combinations

class TestRangeTree(TestCase):
    def test_create(self):
        points = [Point(x, y, 1) for x, y in combinations(range(-10, 10), 2)]
        tree = RangeTree()
        tree.create(points)
        self.assertEqual(len(points), len(tree.traverse()))
        self.assertEqual(set(points), set(tree.traverse()))

    def test_create_null(self):
        points = []
        tree = RangeTree()
        tree.create(points)
        self.assertEqual(len(points), len(tree.traverse()))
        self.assertEqual(set(points), set(tree.traverse()))

    def test_bboxQuery_simple(self):
        points = [
            Point(-2, 1, 1),
            Point(-1, 0, 1),
            Point(-2, 0, 1),
            Point(0, 0, 1),
            Point(1, 0, 1),
            Point(3, 3, 1),
        ]
        correct = [
            Point(-2, 1, 1),
            Point(-1, 0, 1),
            Point(-2, 0, 1),
        ]
        tree = RangeTree()
        tree.create(points)
        bbox = BBox(-2.5, -2, -0.5, 2)
        result = tree.bboxQuery(bbox)
        self.assertEqual(len(result), len(correct))
        self.assertEqual(set(result), set(correct))

    def test_bboxQuery_miss(self):
        points = [
            Point(-2, 1, 1),
            Point(-1, 0, 1),
            Point(-2, 0, 1),
            Point(-2, 0, 1),
            Point(0, 0, 1),
            Point(1, 0, 1),
            Point(3, 3, 1),
        ]
        tree = RangeTree()
        tree.create(points)
        bbox = BBox(5, 5, 7, 7)
        result = tree.bboxQuery(bbox)
        self.assertEqual(result, [])

    def test_bboxQuery_largedata(self):
        points = [Point(x, y, 1) for x, y in combinations(range(-200, 200), 2)]
        correct = list(filter(lambda f: f[0] >= -10 and f[0] <= 10 and f[1] >= -10 and f[1] <= 10, points))
        tree = RangeTree()
        tree.create(points)
        bbox = BBox(-10, -10, 10, 10)
        result = tree.bboxQuery(bbox)
        self.assertEqual(len(result), len(correct))
        self.assertEqual(set(correct), set(result))





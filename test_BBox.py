from unittest import TestCase
from rangetree import Point, BBox

class TestBBox(TestCase):
    def test_fromPoints_emptylist(self):
        points = []
        bbox = BBox.fromPoints(points)
        self.assertEqual(bbox.lowerX, None)
        self.assertEqual(bbox.lowerY, None)
        self.assertEqual(bbox.upperX, None)
        self.assertEqual(bbox.upperY, None)

    def test_fromPoints_onePoint(self):
        points = [Point(0, 1, 1)]
        bbox = BBox.fromPoints(points)
        self.assertEqual(bbox.lowerX, 0)
        self.assertEqual(bbox.lowerY, 1)
        self.assertEqual(bbox.upperX, 0)
        self.assertEqual(bbox.upperY, 1)

    def test_fromPoints_multiPoint(self):
        points = [
            Point(0, 1, 1),
            Point(2, 1, 1),
            Point(-8, 6, 1),
            Point(9, -1, 1),
        ]
        bbox = BBox.fromPoints(points)
        self.assertEqual(bbox.lowerX, -8)
        self.assertEqual(bbox.lowerY, -1)
        self.assertEqual(bbox.upperX, 9)
        self.assertEqual(bbox.upperY, 6)

    def test_isWithin_happyCase(self):
        littleBox = BBox(-1, -1, 1, 1)
        bigBox = BBox(-2, -2, 2, 2)
        self.assertTrue(littleBox.isWithin(bigBox))

    def test_isWithin_overlapping(self):
        oneBox = BBox(0, 0, 1, 1)
        twoBox = BBox(-1,-1, .5, .5)
        self.assertFalse(oneBox.isWithin(twoBox))

    def test_isWithin_nonOverlapping(self):
        oneBox = BBox(1, 1, 2, 2)
        twoBox = BBox(3, 3, 4, 4)
        self.assertFalse(oneBox.isWithin(twoBox))

    def test_isWithin_contains(self):
        littleBox = BBox(-1, -1, 1, 1)
        bigBox = BBox(-2, -2, 2, 2)
        self.assertFalse(bigBox.isWithin(littleBox))


    def test_intersects_within(self):
        littleBox = BBox(-1, -1, 1, 1)
        bigBox = BBox(-2, -2, 2, 2)
        self.assertTrue(littleBox.intersects(bigBox))
        self.assertTrue(bigBox.intersects(littleBox))

    def test_intersects_overlapping(self):
        oneBox = BBox(0, 0, 1, 1)
        twoBox = BBox(-1, -1, .5, .5)
        self.assertTrue(oneBox.intersects(twoBox))
        self.assertTrue(twoBox.intersects(oneBox))

    def test_intersects_nonOverlapping(self):
        oneBox = BBox(1, 1, 2, 2)
        twoBox = BBox(3, 3, 4, 4)
        self.assertFalse(oneBox.intersects(twoBox))
        self.assertFalse(twoBox.intersects(oneBox))



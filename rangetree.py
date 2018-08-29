# TODO: add docstrings

import csv
import os

from enum import Enum
from operator import itemgetter
from collections import defaultdict
class Point(object):
    def __init__(self, x, y, numpoints):
        self.x = x
        self.y = y
        self.numpoints = numpoints

    def __str__(self):
        return 'Point: {{[{0},{1}], {2}}'.format(self.x, self.y, self.numpoints)

    def __key(self):
        return (self.x, self.y, self.numpoints)

    def __repr__(self):
        return str(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __getitem__(self, item):
        return self.__key()[item]

    def heatPoint(self):
        ''' when rendering in leaflet map, we want to present in lat/long order, not x y order.'''
        points = list(self.__key())
        return [points[1], points[0], points[2]]

class Axis(Enum):
    VERTICAL = 0
    HORIZONTAL = 1

    def flipped(self):
        return Axis(not self.value)

class GeometryException(Exception):
    pass

# TODO: add withinRange method
# TODO: change to use points instead of lowerX, lowerY, etc.
class BBox(object):

    def __init__(self, lowerX=None, lowerY=None, upperX=None, upperY=None):
        if not None in (lowerX, lowerY, upperX, upperY):
            try:
                assert(lowerX <= upperX and lowerY <= upperY)
            except:
                raise GeometryException('invalid bounding box.')

        self.lowerX = lowerX
        self.lowerY = lowerY
        self.upperX = upperX
        self.upperY = upperY

    @staticmethod
    def fromPoints(points):
        if len(points) == 0:
            return BBox()
        initpoint = points[0]
        bbox = BBox(initpoint[0], initpoint[1], initpoint[0], initpoint[1])
        for p in points:
            if p.x < bbox.lowerX:
                bbox.lowerX = p.x
            if p.y < bbox.lowerY:
                bbox.lowerY = p.y
            if p.x > bbox.upperX:
                bbox.upperX = p.x
            if p.y > bbox.upperY:
                bbox.upperY = p.y
        return bbox

    def isWithin(self, other):
        return self.lowerX >= other.lowerX and self.lowerY >= other.lowerY \
                and self.upperX <= other.upperX and self.upperY <= other.upperY

    def intersects(self, other):
        xOverlap = self.lowerX <= other.upperX and other.lowerX <= self.upperX
        yOverlap = self.lowerY <= other.upperY and other.lowerY <= self.upperY
        return xOverlap and yOverlap

    def containsPoint(self, point):
        return point.x >= self.lowerX and point.y >= self.lowerY \
                and point.x <= self.upperX and point.y <= self.upperY

    def split(self, point, axis):
        if not self.containsPoint(point):
            raise GeometryException('split line outside of bounding box')
        else:
            if axis == Axis.VERTICAL:
                left = BBox(self.lowerX, self.lowerY, point.x, self.upperY)
                right = BBox(point.x, self.lowerY, self.upperX, self.upperY)
                return (left, right)
            else:
                bottom = BBox(self.lowerX, self.lowerY, self.upperX, point.y)
                top = BBox(self.lowerX, point.y, self.upperX, self.upperY)
                return (bottom, top)

class Node(object):
    def __init__(self, point, axis, bbox, lChild, rChild):
        self.point = point
        self.axis = axis
        self.bbox = bbox
        self.lChild = lChild
        self.rChild = rChild

    def isLeaf(self):
        return self.lChild is None and self.rChild is None

def _traverse(node, callback=lambda p: p.point):
    result = []
    if node:
        result.append(callback(node))
        result += _traverse(node.lChild, callback)
        result += _traverse(node.rChild, callback)
    return result

def _bboxQuery(bbox, node):
    if not node:
        return []
    else:
        if node.bbox.isWithin(bbox):
            return _traverse(node)
        elif node.bbox.intersects(bbox):
            if bbox.containsPoint(node.point):
                return [node.point] + _bboxQuery(bbox, node.lChild) + _bboxQuery(bbox, node.rChild)
            else:
                return _bboxQuery(bbox, node.lChild) + _bboxQuery(bbox, node.rChild)
        else:
            return []


class RangeTree(object):
    '''a range tree is a special case of a k-d tree, involving two dimensions,
    allowing for fast bounding-box queries.'''
    def __init__(self):
        self.root = None

    def create(self, points):
        def partition(axis, bbox, points):
            if not points:
                return None
            # determine split point
            points.sort(key=itemgetter(axis.value))
            medianIndex = len(points) // 2
            splitPoint = points[medianIndex]
            # while medianIndex + 1 < len(points) and points[medianIndex+1][axis.value] == splitPoint[axis.value]:
            #     medianIndex += 1

            leftBox, rightBox = bbox.split(splitPoint, axis)
            newAxis = axis.flipped()

            return Node(splitPoint, axis, bbox,
                        partition(newAxis, leftBox, points[:medianIndex]),
                        partition(newAxis, rightBox, points[medianIndex + 1:]))
        bbox = BBox.fromPoints(points)
        self.root = partition(Axis(0), bbox, points)

    def bboxQuery(self, bbox):
        return _bboxQuery(bbox, self.root)

    def traverse(self):
        return _traverse(self.root)

def countDistinct(iterable, key):
    ''' Where iterable is any Python iterable, and key is a function whose result is hashable.
    Runs over an iterable, counting the number of appearances of key(i) for each i in the iterable.  Returns a
    dictionary of form {key(i): count}'''
    result = defaultdict(int)
    for i in iterable:
        result[key(i)] += 1
    return result

def readPointFile(filename):
    '''Reads the GeoLite City Database file and returns a list of Points.'''
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        latindex = headers.index('latitude')
        longindex = headers.index('longitude')
        points = []
        pointsDict = countDistinct(reader, lambda i: (i[longindex], i[latindex]))
        for k, v in pointsDict.items():
            points.append(Point(float(k[0]), float(k[1]), v))
        # maxpoints = max(points, key=lambda p: p.numpoints).numpoints
        # for p in points:
        #     p. intensity = p.calculateIntensity(maxpoints)
        return points

def main():
    pass

if __name__ == '__main__':
    main()








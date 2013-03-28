import numpy as np
from numpy.linalg import norm
from geometry import Ray, Vector

class Object(object):
    """An object in the scene"""
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return 'Object at {}'.format(str(self.position))

    @property
    def p(self):
        return self.position

class GroundPlane(Object):
    """An infinite flat surface facing a normal"""
    def __init__(self, position=None, normal=None):
        if position is None:
            position = Vector(0, 0, 0)
        if normal is None:
            normal = Vector(0, 1, 0)
        super(GroundPlane, self).__init__(position)
        self.n = normal

    def intersectionDistance(self, ray):
        d = np.dot(self.n, ray.u)
        if d != 0:
            return - (np.dot(self.n, (ray.p - self.p)) / d)
        else:
            return None

    def intersection(self, ray):
        return ray.x(self.intersectionDistance(ray))

class Sphere(Object):
    """A sphere with a position and radius"""
    def __init__(self, position, radius):
        super(Sphere, self).__init__(position)
        self.radius = radius

    def intersectionDistance(self, ray):
        return np.dot(ray.u, (self.p - ray.p))

    def intersects(self, ray):
        x = ray.x(self.intersectionDistance(ray))
        return norm(x-self.position) <= self.radius

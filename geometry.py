import math
import numpy as np

class Ray(object):
    def __init__(self, position, direction):
        self._p = position
        self._u = direction

    @property
    def p(self):
        return self._p

    @property
    def u(self):
        return self._u

    def position(self):
        return self.p

    def direction(self):
        return self.u

    def x(self, t):
        """Return the point t units along the ray"""
        if t is not None:
            return self.p + t * self.u

class Vector(np.ndarray):
    """Shorthand for a three dimensional numpy array"""
    def __new__(self, x, y, z):
        return np.array([x, y, z])

    @classmethod
    def normalize(cls, x, y, z):
        length = math.sqrt(x**2 + y**2 + z**2)
        return cls(x/length, y/length, z/length)

import math
import numpy as np
from numpy.linalg import norm

class Object(object):
    """An object in the scene"""
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return 'Object at {}'.format(str(self.position))

    @property
    def p(self):
        return self.position

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

class Camera(Object):
    """A camera rendering the scene"""
    def __init__(self, position, direction, N=720, M=486,
                 scale=1,
                 orthographic=False):
        super(Camera, self).__init__(position)

        self._orth = orthographic

        self.z_p = 1 #focal length
        self.up = Vector(0, 1, 0)
        self.direction = direction

        #centre of the image screen
        self.c = self.position + self.z_p * self.direction 

        #horizontal screen direction
        self.u_x = (np.cross(self.direction, self.up) /
                   norm(np.cross(self.direction, self.up)))
        #vertical screen direction
        self.u_z = - self.direction
        #normal to the viewscreen
        self.u_y = np.cross(self.u_z, self.u_x)

        self.m = int(M * scale)
        self.n = int(N * scale)

        factor = 0.5
        self.hight = (1)*factor
        self.width = (16/9.0)*factor

        #vertical distance between pixels
        self.dydi = self.hight / float(self.m)
        #horizontal distance between pixels
        self.dxdi = self.width / float(self.n)

    def rays(self):
        """Return a generator containing a ray for each pixel in the image"""
        for i in range(self.m):
            py = -self.hight / 2 + self.dydi * (i + 0.5)
            for j in range(self.n):
                px = -self.width / 2 + self.dxdi * (j + 0.5)

                #pixel center in space
                p = self.c + px * self.u_x + py * self.u_y
                #direction vector
                if self._orth:
                    u = self.direction
                else:
                    u = (p - self.position) / norm(p - self.position)
                yield Ray(p, u)
            yield None #next row

class GroundPlane(Object):
    def __init__(self, position=None, normal=None):
        if position is None:
            position = np.array([0, 0, 0])
        if normal is None:
            normal = np.array([0, 1, 0])
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
    def __init__(self, position, radius):
        super(Sphere, self).__init__(position)
        self.radius = radius

    def intersectionDistance(self, ray):
        return np.dot(ray.u, (self.p - ray.p))

    def intersects(self, ray):
        x = ray.x(self.intersectionDistance(ray))
        return norm(x-self.position) <= self.radius

if __name__ == '__main__':
    import pixmap
    s = Sphere(Vector(0,0,0), 1)
    cpos = Vector(0, 0, 8)
    u = Vector.normalize(0.25, 0, 1)
    print u
    c = Camera(cpos, u, scale=0.25)
    image, row = [], []
    for r in c.rays():
        if r is not None:
            if s.intersects(r):
                row += [[10000, 0, 0]]
            else:
                row += [[65500, 65500, 65500]]
        else:
            image += [row]
            row = []
    pixmap.save(image, 'out/sphere.ppm')

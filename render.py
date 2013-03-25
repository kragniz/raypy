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

class Camera(Object):
    """A camera rendering the scene"""
    def __init__(self, position, direction, N=720, M=486,
                 scale=1,
                 orthographic=False):
        super(Camera, self).__init__(position)

        self._orth = orthographic

        self.z_p = 1 #focal length
        self.up = np.array([0, 1, 0])
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
        super(Plane, self).__init__(position)
        self.n = normal

if __name__ == '__main__':
    import pixmap
    c = Camera(np.array([0, 0, 0]), np.array([0, 0, -1]), scale=0.25,
            orthographic=True)
    r = c.rays()
    rl, row = [], []
    for ray in r:
        if ray is not None:
            row += [np.array([int(4096*(np.dot(ray.u, np.array([0,0,-1]))))]*3)]
        else:
            rl += [np.array(row)]
    pixmap.save(rl, 'vectors.ppm')

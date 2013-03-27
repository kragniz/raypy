import math
import numpy as np
from numpy.linalg import norm
import objects
from geometry import Ray, Vector

class Camera(objects.Object):
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

if __name__ == '__main__':
    import pixmap
    s = objects.Sphere(Vector(0,0,0), 2)
    cpos = Vector(0, 0, 6)
    u = Vector.normalize(0, 0, -1)
    c = Camera(cpos, u, scale=0.25)
    image = []
    l, h = 2**20, 0
    for r in c.rays():
        if r is not None:
            if s.intersects(r):
                col = s.intersectionDistance(r)
                if col > h:
                    h = col
                if col < l:
                    l = col
                image += [col]
            else:
                image += [-1]
        else:
            image += [None]
    row = []
    imagePixels = []
    for p in image:
        if p is not None:
            if p > 0:
                col = int((2**16) * (p-l)/float(h))*5
                row += [[col,col,col]]
            else: row += [[2**16, 0, 0]]
        else:
            imagePixels += [row]
            row = []
    pixmap.save(imagePixels, 'out/sphere.ppm')

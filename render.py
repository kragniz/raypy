# for each pixel:
#    * Compute primary ray direction
#    * Shoot prim ray in the scene
#    * For each object in the scene:
#        * Measure the distance to intersection
#        * Save the object if it's the closest
#    * If an object was found to intersect:
#        * Compute illumination
#        * Find the direction of the shadow rays
#            * position of light - position of the ray intersection 
#        * For each object in the scene:
#            * If the object intersects with the shadow ray:
#                * Mark the point as in shadow
#    * If the point is not in shadow:
#        * Set the pixel value to the colour of the object * brightness of light
#    * else:
#        * Set the pixel value to 0

import numpy as np
from numpy.linalg import norm

class Object(object):
    """An object in the scene"""
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return 'Object at {}'.format(str(self.position))

class Camera(Object):
    """A camera rendering the scene"""
    def __init__(self, position, direction, width=720, hight=486):
        super(Camera, self).__init__(position)
        self.up = np.array([0, 1, 0])
        self.direction = direction

        self.u_x = (np.cross(self.direction, self.up) /
                   norm(np.cross(self.direction, self.up)))
        self.u_z = - self.direction
        self.u_y = np.cross(self.u_z, self.u_x)

if __name__ == '__main__':
    c = Camera(np.array([0, 0, 0]), np.array([0, 0, -1]))
    print c.u_x, c.u_z, c.u_y

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

class Object(object):
    """An object in the scene"""
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return 'Object at {}'.format(str(self.position))

class Camera(Object):
    """A camera rendering the scene"""
    def __init__(self, position, direction):
        super(Camera, self).__init__(position)

if __name__ == '__main__':
    c = Camera(np.array([0, 0, 0]), np.array([0, 0, -1]))

import pygame

from constants import SHIP_HEIGHT, SHIP_WIDTH
from model.point2d import Point2d


class FlyingObject:
    # def __init__(self):
    #     super(FlyingObject, self).__init__()
    #     self.location = Point2d();
    #     self.velocity = Velocity2d();
    #
    #     self.image = pygame.image.load("../assets/images/spaceship.png")

    def __init__(self, location, velocity, image, name="unknown"):
        self.location = location
        self.velocity=velocity
        self.image = pygame.image.load(image)
        self.name=name
        self.width=SHIP_WIDTH
        self.height=SHIP_HEIGHT


    def unit_displacement(self):
        # Displace object by whatever velocity it is having
        self.location.add(self.velocity)

    def mid_point(self):
        return Point2d((self.location.x+SHIP_WIDTH)/2, (self.location.y+SHIP_HEIGHT)/2)

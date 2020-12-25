from constants import BASE_LOCATION, MISSILE_SPEED, SHIP_HALF_WIDTH, SHIP_HALF_HEIGHT
from model.flying_object import FlyingObject
from model.missile import Missile
from model.point2d import Point2d
from model.velocity2d import Velocity2d


class Alien(FlyingObject):
    def __init__(self, location, velocity, image, name="alien"):
        super().__init__(location, velocity, image, name="Alien")
        self.alive = True

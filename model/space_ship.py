from constants import BASE_LOCATION, MISSILE_SPEED, SHIP_HALF_WIDTH, SHIP_HALF_HEIGHT
from model.flying_object import FlyingObject
from model.missile import Missile
from model.point2d import Point2d
from model.velocity2d import Velocity2d


class SpaceShip(FlyingObject):
    def __init__(self, location, velocity, image, name="unknown"):
        super().__init__(location, velocity, image, name="Spaceship")
        missileLoction = Point2d(location.x, location.y)
        missileLoction.add(Point2d(SHIP_HALF_WIDTH, 0))
        self.missile = Missile(missileLoction,
                               Velocity2d(0,0),
                               BASE_LOCATION + "assets\\images\\missile.png")
        self.score = 0
        self.lives = 3

    def fire_missile(self):
        self.missile.location.set(self.location)
        self.missile.location.add(Point2d(SHIP_HALF_WIDTH, SHIP_HALF_HEIGHT))
        self.missile.velocity.set(self.velocity)
        self.missile.velocity.add(Velocity2d(0, MISSILE_SPEED))
        self.missile.state = "fire"

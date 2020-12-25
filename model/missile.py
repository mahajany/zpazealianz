from model.flying_object import FlyingObject
from model.point2d import Point2d


class Missile(FlyingObject):
    def __init__(self, location, velocity, image, name="unknown"):
        super().__init__(location, velocity, image, name="Missile")
        self.state = "ready"
#Ready - can't see, Fire-Moving

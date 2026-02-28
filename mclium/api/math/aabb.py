from mclium.api.math.vec3 import Vec3
class AABB:
    def __init__(self, min_v: Vec3, max_v: Vec3):
        self.min = min_v
        self.max = max_v

    def intersects(self, other):
        return (
            self.min.x <= other.max.x and
            self.max.x >= other.min.x and
            self.min.y <= other.max.y and
            self.max.y >= other.min.y and
            self.min.z <= other.max.z and
            self.max.z >= other.min.z
        )

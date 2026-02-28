class Rotation:
    def __init__(self, yaw,pitch):
        self.yaw = yaw
        self.pitch = pitch

    def clamp(self):
        self.pitch = max(min(self.pitch,360), 0)


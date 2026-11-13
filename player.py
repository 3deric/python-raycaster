from pyray import *
from raylib import *
import math

class Player():
    def __init__(self, pos : Vector2):
        self.pos : Vector2 = pos
        self.speed : float = 1.0
        self.rot : float = 0
        self.rot_speed : float = 50.0
        self.dir : Vector2 = Vector2(0, 0)
        self.radius : float = 10.0
        self.input : Vector2 = Vector2(0, 0)
        self.color = RED
        self.ray_color = YELLOW
        self.fov = 45

    def move(self, delta: float):
        self.input.x = int(IsKeyDown(KEY_D)) - int(IsKeyDown(KEY_A))
        self.input.y = int(IsKeyDown(KEY_W)) - int(IsKeyDown(KEY_S))
        self.rot += self.input.x * self.rot_speed * delta
        self.dir.x = math.cos(math.radians(self.rot))
        self.dir.y = math.sin(math.radians(self.rot))
        self.pos.x += self.dir.x * self.speed * self.input.y * delta
        self.pos.y += self.dir.y * self.speed * self.input.y * delta


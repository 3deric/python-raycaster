from pyray import *
from raylib import *
import math
import random

WINDOW_NAME = 'Python Raycasting'
WINDOW_WIDTH : int = 1200
WINDOW_HEIGHT :int = 1000
WINDOW_CLEAR_COLOR : Color = BLACK
GRID_SIZE : int = 100
GRID_COLOR : Color = DARKGRAY
RAY_DRAW_LEN : float = 1.0

class Player():
    def __init__(self, pos : Vector2):
        self.pos : Vector2 = pos
        self.speed : float = 1.0
        self.rot : float = 0
        self.rot_speed : float = 50.0
        self.dir : Vector2 = Vector2(0, 0)
        self.radius : float = 10.0
        self.input : Vector2 = Vector2(0, 0)
        self.colour = RED
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

    def draw(self):
        draw_circle(int(self.pos.x * GRID_SIZE), int(self.pos.y * GRID_SIZE), self.radius, self.colour)

        draw_line(int(self.pos.x * GRID_SIZE), int(self.pos.y * GRID_SIZE), int(self.pos.x * GRID_SIZE) + int(self.dir.x * GRID_SIZE),int(self.pos.y * GRID_SIZE) + int(self.dir.y * GRID_SIZE), GREEN)

    def draw_rays(self, grid):
        for i in range(int(self.rot - self.fov/2), int(self.rot + self.fov/2), 5):
            dir = Vector2(0,0)
            dir.x = math.cos(math.radians(i))
            dir.y = math.sin(math.radians(i))
            self.draw_ray(dir, grid)

    def draw_ray(self, dir, grid):
        # current grid element of map
        map_x : int = int(self.pos.x)
        map_y : int = int(self.pos.y)

        # length of ray from current position to next x or y-side
        side_dist_x : float = 0
        side_dist_y : float = 0

        # length of ray from one x or y-side to next x or y-side
        delta_dist_x : float = 999999.9 if dir.x == 0 else math.fabs(1/dir.x)
        delta_dist_y : float = 999999.9 if dir.y == 0 else math.fabs(1/dir.y)

        # direction for next move (-1 or 1)
        step_x : int = 0
        step_y : int = 0

        if dir.x < 0:
            step_x = -1
            side_dist_x = (self.pos.x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - self.pos.x) * delta_dist_x
        if dir.y < 0:
            step_y = -1
            side_dist_y = (self.pos.y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - self.pos.y) * delta_dist_y

        steps = 0
        hit = False

        while(steps < 10):
            # jump to next map square, eather in x-direction, or in y-direction
            if side_dist_x < side_dist_y:
                distance = side_dist_x
                side_dist_x += delta_dist_x
                map_x += step_x
            else:
                distance = side_dist_y
                side_dist_y += delta_dist_y
                map_y += step_y

            steps += 1
            circle_x = (self.pos.x + dir.x * distance) * GRID_SIZE
            circle_y = (self.pos.y + dir.y * distance) * GRID_SIZE
            if grid.get_value(map_x, map_y):
                steps = 10
                draw_circle(int(circle_x), int(circle_y), 4, GREEN)
            else:
                draw_circle(int(circle_x), int(circle_y), 2, DARKGREEN)

class Grid():
    def __init__(self):
        self.grid : list = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def draw(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    draw_rectangle(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_COLOR)
                else:
                    draw_rectangle_lines(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_COLOR)

    def get_value(self, x, y) -> bool:
        return True if self.grid[y][x] == 1 else False

# Create Raylib Window
init_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME)
grid = Grid()
player = Player(Vector2(1,1))

# Raylib Main Loop
while not window_should_close():
    #game logic
    dt : float = get_frame_time()
    player.move(dt)
    #game drawing
    begin_drawing()
    clear_background(WINDOW_CLEAR_COLOR)
    grid.draw()
    player.draw()
    player.draw_rays(grid)
    draw_fps(10, 10)
    end_drawing()
close_window()
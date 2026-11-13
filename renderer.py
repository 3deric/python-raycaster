from pyray import *
from raylib import *
import math

GRID_SIZE : int = 20
GRID_COLOR : Color = DARKGRAY

class Renderer:
    def __init__(self, grid, player):
        self.grid = grid
        self.player = player

    def draw(self):
       # self._draw_viewport()
        self._draw_minimap()

    def _draw_minimap(self):
        self._draw_grid()
        self._draw_rays()
        self._draw_player()

    def _draw_grid(self):
        for y in range(len(self.grid.grid)):
            for x in range(len(self.grid.grid[y])):
                if self.grid.grid[y][x] == 1:
                    draw_rectangle(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_COLOR)
                else:
                    draw_rectangle_lines(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_COLOR)

    def _draw_player(self):
        draw_circle(int(self.player.pos.x * GRID_SIZE), int(self.player.pos.y * GRID_SIZE), self.player.radius, self.player.color)
        #draw_line(int(self.player.pos.x * GRID_SIZE), int(self.player.pos.y * GRID_SIZE), int(self.player.pos.x * GRID_SIZE) + int(self.player.dir.x * GRID_SIZE),int(self.player.pos.y * GRID_SIZE) + int(self.player.dir.y * GRID_SIZE), self.player.color)

    def _draw_rays(self):
        for i in range(int(self.player.rot - self.player.fov/2), int(self.player.rot + self.player.fov/2), 5):
            dir = Vector2(0,0)
            dir.x = math.cos(math.radians(i))
            dir.y = math.sin(math.radians(i))
            self._draw_ray(dir, self.grid)

    def _draw_ray(self, dir, grid):
        pos_x = self.player.pos.x
        pos_y = self.player.pos.y
        # current grid element of map
        map_x: int = int(pos_x)
        map_y: int = int(pos_y)

        # length of ray from one x or y-side to next x or y-side
        delta_dist_x: float = 999999.9 if dir.x == 0 else math.fabs(1 / dir.x)
        delta_dist_y: float = 999999.9 if dir.y == 0 else math.fabs(1 / dir.y)

        # side_dist_x and y is length of ray from current position to next x or y-side
        # step is the direction for the next move in x and y direction
        if dir.x < 0:
            step_x = -1
            side_dist_x = (pos_x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - pos_x) * delta_dist_x
        if dir.y < 0:
            step_y = -1
            side_dist_y = (pos_y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - pos_y) * delta_dist_y

        steps = 0
        hit = False

        while steps < 10 and hit == False:
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
            circle_x = int((pos_x + dir.x * distance) * GRID_SIZE)
            circle_y = int((pos_y + dir.y * distance) * GRID_SIZE)
            if grid.get_value(map_x, map_y):
                hit = True
                #draw_circle(circle_x, circle_y, 4, GREEN)
            draw_line(int(pos_x * GRID_SIZE), int(pos_y * GRID_SIZE), circle_x, circle_y, GREEN)
            # else: # circles on all inbetween gridlines
            #    draw_circle(circle_x, circle_y, 2, DARKGREEN)

    def _draw_viewport(self):
        dir = Vector2(0, 0)
        dir.x = math.cos(math.radians(self.player.rot))
        dir.y = math.sin(math.radians(self.player.rot))
        self._draw_slice(dir, self.grid)

    def _draw_slice(self, dir, grid):
        pos_x = self.player.pos.x
        pos_y = self.player.pos.y

        map_x: int = int(pos_x)
        map_y: int = int(pos_y)

        delta_dist_x: float = 999999.9 if dir.x == 0 else math.fabs(1 / dir.x)
        delta_dist_y: float = 999999.9 if dir.y == 0 else math.fabs(1 / dir.y)

        if dir.x < 0:
            step_x = -1
            side_dist_x = (pos_x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - pos_x) * delta_dist_x
        if dir.y < 0:
            step_y = -1
            side_dist_y = (pos_y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - pos_y) * delta_dist_y

        steps = 0
        hit = False

        while (steps < 10 and hit == False):
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
            circle_x = int((pos_x + dir.x * distance) * GRID_SIZE)
            circle_y = int((pos_y + dir.y * distance) * GRID_SIZE)
            if grid.get_value(map_x, map_y):
                hit = True
                draw_circle(circle_x, circle_y, 4, GREEN)
                draw_line(int(pos_x * GRID_SIZE), int(pos_y * GRID_SIZE), circle_x, circle_y, GREEN)
            # else: # circles on all inbetween gridlines
            #    draw_circle(circle_x, circle_y, 2, DARKGREEN)
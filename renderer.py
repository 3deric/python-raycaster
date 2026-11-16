from pyray import *
from raylib import *
import math

GRID_SIZE : int = 20
GRID_COLOR : Color = DARKGRAY
MINIMAP_RAYS : int = 10
VIEWPORT_RAYS : int = 200
RAYS : int = 500

class Renderer:
    def __init__(self, grid, player, width, height):
        self.grid = grid
        self.player = player
        self.width = width
        self.height = height

        # values for rendering the viewport and minimap
        self.ray_distances = [0.0] * RAYS
        self.ray_side =[0] * RAYS
        self.ray_dir = [0.0] * RAYS
        self.hits = [False] * RAYS

        self.start_angle = self.player.rot - self.player.fov / 2
        self.ray_step = self.player.fov / (RAYS - 1)
        self.viewport_step = self.player.fov / (self.width - 1)

    def draw(self):
        self._cast_rays()
        self._draw_viewport()
        self._draw_minimap()

    def _draw_minimap(self):
        self._draw_grid_minimap()
        self._draw_rays_minimap()
        self._draw_player_minimap()

    def _draw_grid_minimap(self):
        draw_rectangle(0,0,len(self.grid.grid[0]) * GRID_SIZE, len(self.grid.grid) * GRID_SIZE, BLACK)
        for y in range(len(self.grid.grid)):
            for x in range(len(self.grid.grid[y])):
                if self.grid.grid[y][x] == 1:
                    draw_rectangle(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_COLOR)
                else:
                    draw_rectangle_lines(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_COLOR)

    def _draw_player_minimap(self):
        draw_circle(int(self.player.pos.x * GRID_SIZE), int(self.player.pos.y * GRID_SIZE), self.player.radius, self.player.color)
        draw_line(int(self.player.pos.x * GRID_SIZE), int(self.player.pos.y * GRID_SIZE), int(self.player.pos.x * GRID_SIZE) + int(self.player.dir.x * GRID_SIZE),int(self.player.pos.y * GRID_SIZE) + int(self.player.dir.y * GRID_SIZE), self.player.color)

    def _draw_rays_minimap(self):
        indices = [i * (len(self.ray_distances) - 1) // (MINIMAP_RAYS - 1) for i in range(MINIMAP_RAYS)]
        for i in indices:
            dir = self.ray_dir[i]
            dist = self.ray_distances[i]
            end_x = int((self.player.pos.x + dir.x * dist) * GRID_SIZE)
            end_y = int((self.player.pos.y + dir.y * dist) * GRID_SIZE)
            draw_line(int(self.player.pos.x * GRID_SIZE), int(self.player.pos.y * GRID_SIZE), end_x, end_y, GREEN)

    def _draw_viewport(self):
        indices = [i * (len(self.ray_distances) - 1) // (VIEWPORT_RAYS - 1) for i in range(VIEWPORT_RAYS)]
        for i in indices:
            if self.hits[i] == False:
                continue
            dist = self.ray_distances[i]
            side = self.ray_side[i]
            x = int(i * self.width / indices[-1])
            #self._draw_line(x, side, dist)
            self._draw_rect(x, side, dist)

    def _cast_rays(self):
        ray_angles = [self.start_angle + i * self.ray_step for i in range(RAYS)]
        for i, angle in enumerate(ray_angles):
            dir = Vector2(0, 0)
            dir.x = math.cos(math.radians(angle + self.player.rot))
            dir.y = math.sin(math.radians(angle + self.player.rot))
            self._cast_ray(i, dir, self.grid)

    def _cast_ray(self, i, dir, grid):
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

        while steps < 20 and hit == False:
            # jump to next map square, eather in x-direction, or in y-direction
            if side_dist_x < side_dist_y:
                distance = side_dist_x
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                distance = side_dist_y
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            steps += 1
            if grid.get_value(map_x, map_y):
                hit = True
        self.ray_side[i] = side
        self.ray_distances[i] = distance
        self.ray_dir[i] = dir
        self.hits[i] = hit

    def _draw_line(self, i, side, dist):
        if dist == 0:
            return
        line_h = int(1000 / dist)
        if line_h > 1000:
            line_h = 1000
        line_shade = clamp(1 - (dist / 10), 0,1)
        line_color = color_from_hsv(120, 0.5, line_shade) if side == 1 else color_from_hsv(30, 0.5, line_shade)
        draw_line(i, int(self.height/2 - line_h / 2), i , int(self.height/2 + line_h / 2), line_color)

    def _draw_rect(self, i, side, dist):
        if dist == 0:
            return
        line_h = int(1000 / dist)
        if line_h > 1000:
            line_h = 1000
        rect_shade = clamp(1 - (dist / 10), 0,1)
        rect_color = color_from_hsv(120, 0.5, rect_shade) if side == 1 else color_from_hsv(30, 0.5, rect_shade)
        draw_rectangle(i, int(self.height/2 - line_h / 2), int(self.width / VIEWPORT_RAYS) + 2, int(line_h), rect_color)
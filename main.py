from pyray import *
from raylib import *
import grid, player, renderer

WINDOW_NAME = 'Python Raycasting'
WINDOW_WIDTH  : int = 1200
WINDOW_HEIGHT : int = 1000
WINDOW_CLEAR_COLOR : Color = BLACK

# Create Raylib Window
window = init_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME)
grid = grid.Grid()
player = player.Player(Vector2(1,1))
renderer = renderer.Renderer(grid, player)

# Raylib Main Loop
while not window_should_close():
    #game logic
    dt : float = get_frame_time()
    player.move(dt)
    #game drawing
    begin_drawing()
    clear_background(WINDOW_CLEAR_COLOR)
    renderer.draw()
    draw_fps(10, 10)
    end_drawing()
close_window()
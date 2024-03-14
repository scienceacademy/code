import random

NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
neighbors = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0),
             EAST: (1, 0)}
width, height = 40, 20

# This defines a single cell with four walls
class Cell:
    def __init__(self):
        self.walls = {NORTH: True, SOUTH: True, WEST: True, EAST: True}
        self.visited = False

# Creates the maze as a grid of cells
maze = [[Cell() for x in range(width)] for y in range(height)]

# This function "carves" the path out of the grid.
def carve(x, y):
    # TODO: Complete the DFS algorithm
    pass

# Choose the starting position
startx, starty = 0, 0
carve(startx, starty)
save_file = "maze"
pixel_size = 25

# DO NOT CHANGE BELOW THIS LINE
#############################
import svgwrite
import cairosvg
import os
def maze_to_svg(cell_size):
    dwg = svgwrite.Drawing(
        size=(len(maze[0]) * cell_size, len(maze) * cell_size))

    # create the styles for walls and paths
    dwg.defs.add(dwg.style(
        '.wall {stroke: green; stroke-width: 4;} .path {stroke: white; stroke-width: 2;}'))

    # background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=None, ry=None, fill="rgb(50, 50, 50)"))
    # draw the walls and paths
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x].walls[NORTH]:
                dwg.add(dwg.line((x * cell_size, y * cell_size),
                        ((x + 1) * cell_size, y * cell_size), class_='wall'))
            if maze[y][x].walls[SOUTH]:
                dwg.add(dwg.line((x * cell_size, (y + 1) * cell_size),
                        ((x + 1) * cell_size, (y + 1) * cell_size), class_='wall'))
            if maze[y][x].walls[WEST]:
                dwg.add(dwg.line((x * cell_size, y * cell_size),
                        (x * cell_size, (y + 1) * cell_size), class_='wall'))
            if maze[y][x].walls[EAST]:
                dwg.add(dwg.line(((x + 1) * cell_size, y * cell_size),
                        ((x + 1) * cell_size, (y + 1) * cell_size), class_='wall'))
            if maze[y][x].visited:
                dwg.add(dwg.line((x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
                        (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), class_='path'))

    return dwg.tostring()

svg = maze_to_svg(pixel_size)

with open(save_file+".svg", "w") as f:
    f.write(svg)
cairosvg.svg2png(url=save_file+".svg", write_to=save_file+".png")
os.remove(save_file+".svg")

import os
import cairosvg
import svgwrite
import random

NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
directions = [NORTH, SOUTH, EAST, WEST]
opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
neighbors = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0), EAST: (1, 0)}
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
    ### TODO: Paste your carve function here
    pass

def heuristic(cell, goal):
    # Calculate the Manhattan distance as a heuristic
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

def sort_by_cost(cell_list):
    return sorted(cell_list, key=lambda x: x[0], reverse=True)


def solve(start, end):
    # List of cells to be checked
    cell_list = []

    # Add the starting cell onto the cell list
    # with (cost, cell coordinates, parent cell)
    cell_list.append( (0, start, None) )

    # Initialize a dictionary to store the cost and parent of each cell visited
    cost_so_far = {start: 0}
    parent = {start: None}
    #----------------------------
    # TODO: Your code starts here


    # TODO: Your code ends here
    #--------------------------

    # Trace back the path from end to start (for drawing)
    path = []
    current = end
    while current:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

# Choose the starting position and carve the maze
startx, starty = 0, 0
carve(startx, starty)
save_file = "maze"
pixel_size = 25

# You can knock down some random walls here

# Solve the maze
endx, endy = width-1, height-1
solution = solve( (startx, starty), (endx, endy) )
print(len(solution))
# DO NOT CHANGE BELOW THIS LINE
#############################


def maze_to_svg(cell_size):
    dwg = svgwrite.Drawing(
        size=(len(maze[0]) * cell_size, len(maze) * cell_size))

    # create the styles for walls and paths
    dwg.defs.add(dwg.style(
        '.wall {stroke: green; stroke-width: 4;} .path {stroke: none; fill: goldenrod; stroke-width: 2;}'))
    # background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"),
            rx=None, ry=None, fill="rgb(50, 50, 50)"))
    # draw the walls and paths
    for x, y in solution:
        dwg.add(dwg.rect((x * cell_size + 0, y * cell_size + 0),
                         (cell_size - 0, cell_size - 0),
                         class_="path"))
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
            # if maze[y][x].visited:
            #     dwg.add(dwg.line((x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
            #             (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), class_='path'))
            # if maze[y][x].solved:
            #     dwg.add(dwg.line((x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
            #             (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), class_='path'))

    return dwg.tostring()


svg = maze_to_svg(pixel_size)

with open(save_file+".svg", "w") as f:
    f.write(svg)
cairosvg.svg2png(url=save_file+".svg", write_to=save_file+".png")
os.remove(save_file+".svg")

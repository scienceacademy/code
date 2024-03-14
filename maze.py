from xml.dom.minidom import Document
import random

NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
directions = [NORTH, SOUTH, EAST, WEST]
opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
neighbors = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0),
             EAST: (1, 0)}
class Cell:
    def __init__(self):
        self.walls = {NORTH: True, SOUTH: True, WEST: True, EAST: True}
        self.visited = False

def generate_maze(width, height):
    # create a maze of cells with walls on all sides
    # cell = {'N': True, 'S': True, 'W': True, 'E': True, 'visited': False}
    maze = [[Cell() for y in range(height)] for x in range(width)]

    def carve(x, y):
        # TODO: Complete the DFS algorithm - see instructions
        # Your code goes between these lines
        # ---------------------------------------------------



        # ---------------------------------------------------
        pass
  carve(0, 0)
  return maze


def maze_to_svg(maze, cell_size):
    # create the XML document and root element
    doc = Document()
    svg = doc.createElement('svg')
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    svg.setAttribute('width', str(len(maze) * cell_size))
    svg.setAttribute('height', str(len(maze[0]) * cell_size))
    doc.appendChild(svg)

    # create the styles for walls and paths
    styles = doc.createElement('style')
    styles.appendChild(doc.createTextNode('''
        .wall {
            stroke: green;
            stroke-width: 2;
        }
        .path {
            stroke: white;
            stroke-width: 2;
        }
    '''))
    svg.appendChild(styles)

    # draw the walls and paths
    for y in range(len(maze[0])):
        for x in range(len(maze)):
            if maze[x][y].walls[NORTH]:
                wall = doc.createElement('line')
                wall.setAttribute('class', 'wall')
                wall.setAttribute('x1', str(x * cell_size))
                wall.setAttribute('y1', str(y * cell_size))
                wall.setAttribute('x2', str((x + 1) * cell_size))
                wall.setAttribute('y2', str(y * cell_size))
                svg.appendChild(wall)
            if maze[x][y].walls[SOUTH]:
                wall = doc.createElement('line')
                wall.setAttribute('class', 'wall')
                wall.setAttribute('x1', str(x * cell_size))
                wall.setAttribute('y1', str((y + 1) * cell_size))
                wall.setAttribute('x2', str((x + 1) * cell_size))
                wall.setAttribute('y2', str((y + 1) * cell_size))
                svg.appendChild(wall)
            if maze[x][y].walls[WEST]:
                wall = doc.createElement('line')
                wall.setAttribute('class', 'wall')
                wall.setAttribute('x1', str(x * cell_size))
                wall.setAttribute('y1', str(y * cell_size))
                wall.setAttribute('x2', str(x * cell_size))
                wall.setAttribute('y2', str((y + 1) * cell_size))
                svg.appendChild(wall)
            if maze[x][y].walls[EAST]:
                wall = doc.createElement('line')
                wall.setAttribute('class', 'wall')
                wall.setAttribute('x1', str((x + 1) * cell_size))
                wall.setAttribute('y1', str(y * cell_size))
                wall.setAttribute('x2', str((x + 1) * cell_size))
                wall.setAttribute('y2', str((y + 1) * cell_size))
                svg.appendChild(wall)
            if maze[x][y].visited:
                path = doc.createElement('line')
                path.setAttribute('class', 'path')
                path.setAttribute('x1', str(x * cell_size + cell_size // 2))
                path.setAttribute('y1', str(y * cell_size + cell_size // 2))
                path.setAttribute('x2', str(x * cell_size + cell_size // 2))
                path.setAttribute('y2', str(y * cell_size + cell_size // 2))
                svg.appendChild(path)

    return doc.toprettyxml()

maze = generate_maze(40, 20)
svg = maze_to_svg(maze, 20)

with open("maze1.svg", "w") as f:
    f.write(svg)

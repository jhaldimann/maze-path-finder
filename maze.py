import numpy as np
from numpy import ndarray
import sys


class Maze:
    maze = None
    start = None
    end = None
    visited_nodes = None
    path = None
    result_path = ""

    """
    Constructor for the Maze class
    
    :param path:    Path to the file of the maze     
    """
    def __init__(self, path):
        self.path = path
        # Read the maze structure of the file
        self.maze = self.read_maze(self.path)

    """
    Read the maze file from given input
    
    :param path:        Path to the file of the maze 
    :return ndarray:    Returns a new generated numpy array 
    """
    def read_maze(self, path) -> ndarray:
        # Use file library to open and read file
        try:
            with open(path, "r") as f:
                l = f.readlines()
                m = []
                # Loop over all lines and map every value
                for i in range(len(l)):
                    l[i] = l[i].replace('\n', '')
                    row = []
                    # Map the existing characters with numbers
                    for j in range(len(l[i])):
                        if l[i][j] == '*':
                            row.append(0)
                        elif l[i][j] == ' ':
                            row.append(1)
                        elif l[i][j] == 'A':
                            self.start = [i, j]
                            row.append(2)
                        elif l[i][j] == 'B':
                            self.end = [i, j]
                            row.append(3)
                    m.append(row)

                # Create new 2D numpy array
                arr = np.array(m, dtype=str)

                f.close()
                return arr
        except IOError:
            print("Oh no I can't read the file :(")
            # Exit the application
            sys.exit()

    """
    Find a path in an existing maze
    """
    def find_path_in_maze(self):
        # Check if maze was loaded
        if self.maze is not None:
            # Define the visited node 2D Array
            self.visited_nodes = np.zeros((self.maze.shape[0], self.maze.shape[1]), dtype=bool)
            # If there is a solution ...
            if self.visit_pos(self.start[0], self.start[1]):
                print("Printed Maze")
            else:
                print("No Path found")

    """
    Visit single node in the maze with floodfill method
    
    :param x:       The x coordinate of the node
    :param y:       The y coordinate of the node 
    :return bool:   Return true or false if path is completed 
    """
    def visit_pos(self, x, y) -> bool:
        # Basecheck if position is the end
        if x == self.end[0] and y == self.end[1]:
            return True

        # Set the actual node to visited
        self.visited_nodes[x][y] = True
        result = False

        # Go to next pos in eastern direction
        if not self.visited_nodes[x, y + 1] and self.maze[x][y + 1] != "0":
            new_pos = self.visit_pos(x, y + 1)
            if new_pos:
                self.maze[x][y + 1] = 4
                self.result_path += "E"
            result = new_pos or result

        # Go to next pos in western direction
        if not self.visited_nodes[x, y - 1] and self.maze[x][y - 1] != "0":
            new_pos = self.visit_pos(x, y - 1)
            if new_pos:
                self.maze[x][y - 1] = 5
                self.result_path += "W"
            result = new_pos or result

        # Go to next pos in southern direction
        if not self.visited_nodes[x + 1, y] and self.maze[x + 1][y] != "0":
            new_pos = self.visit_pos(x + 1, y)
            if new_pos:
                self.maze[x + 1][y] = 6
                self.result_path += "S"
            result = new_pos or result

        # Go to next pos in northward direction
        if not self.visited_nodes[x - 1, y] and self.maze[x - 1][y] != "0":
            new_pos = self.visit_pos(x - 1, y)
            if new_pos:
                self.maze[x - 1][y] = 7
                self.result_path += "N"
            result = new_pos or result

        return result

    """
    Print the new generated with the path inside
    It should be mapped like the old maze
    """
    def print_maze_with_path(self):
        # Loop over all entries in the 2D Array
        for i in range(0, self.maze.shape[0]):
            row = ""
            for j in range(0, self.maze.shape[1]):
                # Map the values from the array with the corresponding char
                if self.maze[i][j] == "0":
                    row += '*'
                elif self.maze[i][j] == "1":
                    row += ' '
                elif self.maze[i][j] == "2":
                    row += 'A'
                elif self.maze[i][j] == "3":
                    row += 'B'
                elif self.maze[i][j] == "4":
                    row += 'E'
                elif self.maze[i][j] == "5":
                    row += 'W'
                elif self.maze[i][j] == "6":
                    row += 'S'
                elif self.maze[i][j] == "7":
                    row += 'N'
            # Print row by row
            print(row)


if __name__ == "__main__":
    # Check if a file is provided as argument
    if len(sys.argv) > 1:
        print("--------- Find Path inside of the Maze ---------")
        maze = Maze(sys.argv[1])
        maze.find_path_in_maze()
        maze.print_maze_with_path()
        print('\n')
        print("--------- The Path to exit the Maze is: ---------")
        print(maze.result_path[::-1])
    else:
        print("You have to add a file as parameter")

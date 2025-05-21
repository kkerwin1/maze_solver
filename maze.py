from widgets import Cell, Line, Point
from constants import ROUTE_COLOR, UNDO_COLOR

import time, random

class Maze:
    """
    Defines maze

    :param x1: x coordinate of top-left corner of the maze
    :type x1: int

    :param y1: y coordinate of top-left corner of the maze
    :type y1: int

    :param num_cols: Number of columns of cells in maze
    :type num_cols: int

    :param num_rows: Number of rows of cells in maze
    :type num_rows: int

    :param cell_size_x: Width of cells
    :type cell_size_x: int

    :param win: Window
    :type win: gui.Window
    """

    def __init__(
            self, x1, y1, num_cols, num_rows,
            cell_size_x, cell_size_y, win=None, seed=None
    ):
        
        # We use a constant seed for testing purposes
        if seed:
            random.seed(seed)

        self.x1 = x1
        self.y1 = y1
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self.cells = []
        self.__create_cells()
    
    def __create_cells(self):
        """
        Create maze cells.
        """

        # Create down columns first, across second
        for i in range(0, self.num_cols):
            column = []
            for j in range(0, self.num_rows):
                column.append(Cell(self.win))
            self.cells.append(column)
        
        # Animate across rows first, down second
        for j in range(0, self.num_rows):
            for i in range(0, self.num_cols):
                self.__draw_cell(i, j)
        
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()
        self.solve()
        
    def __draw_cell(self, i, j):
        """
        Given matrix coordinates of a cell, calculate x,y coordinates of cell and draw it.

        :param i: Column number
        :type i: int

        :param j: Row number
        :type j: int
        """

        cell = self.cells[i][j]
        x1 = self.x1 + (i * self.cell_size_x)
        y1 = self.y1 + (j * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        cell.draw(x1, y1, x2, y2)
        self.animate_cells()
    
    def __break_entrance_and_exit(self):
        """
        Cut entrance in top wall of the cell in the top-left corner, and cut exit in bottom wall of the cell in the bottom-right corner.
        """

        entrance_cell = self.cells[0][0]
        entrance_cell.has_top_wall = False
        self.__draw_cell(0, 0)

        j = len(self.cells[0])-1
        i = len(self.cells)-1
        exit_cell = self.cells[i][j]
        exit_cell.has_bottom_wall = False
        self.__draw_cell(i, j)
    
    def __reset_cells_visited(self):
        """
        Reset all cells' visited status after drawing the maze, and before solving it.
        """

        for column in self.cells:
            for cell in column:
                cell.visited = False
    
    def __break_walls_r(self, i, j):
        """
        Recursive function to break walls and create a solvable maze.

        :param i: Column number
        :type i: int

        :param j: Row number
        :type j: int
        """

        cell = self.cells[i][j]
        cell.visited = True
        while True:
            to_visit = []
            possible = {}

            if i > 0:
                left = self.cells[i-1][j]
                if not left.visited:
                    possible["left"] = left
            if j > 0:
                up = self.cells[i][j-1]
                if not up.visited:
                    possible["up"] = up
            if i <= len(self.cells)-2:
                right = self.cells[i+1][j]
                if not right.visited:
                    possible["right"] = right
            if j <= len(self.cells[0])-2:
                down = self.cells[i][j+1]
                if not down.visited:
                    possible["down"] = down
            
            if len(possible) == 0:
                return
            else:
                direction = random.choice(list(possible.keys()))
                destination = possible[direction]

                if direction == "left":
                    cell.has_left_wall = False
                    destination.has_right_wall = False
                    self.__draw_cell(i, j)
                    self.__draw_cell(i-1, j)
                    self.__break_walls_r(i-1, j)
                elif direction == "up":
                    cell.has_top_wall = False
                    destination.has_bottom_wall = False
                    self.__draw_cell(i, j)
                    self.__draw_cell(i, j-1)
                    self.__break_walls_r(i, j-1)
                elif direction == "right":
                    cell.has_right_wall = False
                    destination.has_left_wall = False
                    self.__draw_cell(i, j)
                    self.__draw_cell(i+1, j)
                    self.__break_walls_r(i+1, j)
                elif direction == "down":
                    cell.has_bottom_wall = False
                    destination.has_top_wall = False
                    self.__draw_cell(i, j)
                    self.__draw_cell(i, j+1)
                    self.__break_walls_r(i, j+1)

    def solve(self):
        """
        Entrypoint to solve the maze.
        """

        return self.__solve_r(0, 0)
    
    def __solve_r(self, i, j):
        """
        Recursively called to solve the maze.

        :param i: Column number
        :type i: int

        :param j: Row number
        :type j: int
        """

        self.animate_cells()
        cell = self.cells[i][j]
        cell.visited = True
        status = False

        # We're at the end cell
        if (i == len(self.cells)-1) and (j == len(self.cells[0])-1):
            status = True
            return status
        else:
            possible = {}
            if i > 0:
                left = self.cells[i-1][j]
                if (not left.visited) and not (cell.has_left_wall):
                    possible["left"] = (left, (i-1, j))
            if j > 0:
                up = self.cells[i][j-1]
                if (not up.visited) and not (cell.has_top_wall):
                    possible["up"] = (up, (i, j-1))
            if i <= len(self.cells)-2:
                right = self.cells[i+1][j]
                if (not right.visited) and not (cell.has_right_wall):
                    possible["right"] = (right, (i+1, j))
            if j <= len(self.cells[0])-2:
                down = self.cells[i][j+1]
                if (not down.visited) and not (cell.has_bottom_wall):
                    possible["down"] = (down, (i, j+1))
            
            for direction in possible.keys():
                destination = possible[direction][0]
                i, j = possible[direction][1]
                x1, y1 = cell.center_x, cell.center_y
                x2, y2 = destination.center_x, destination.center_y
                point1 = Point(x1, y1)
                point2 = Point(x2, y2)
                line = Line(point1, point2)
                self.win.draw_line(line, ROUTE_COLOR)
                status = self.__solve_r(i, j)
                if status:
                    return True
                else:
                    self.win.draw_line(line, UNDO_COLOR)
            if not status:
                return False

    def animate_cells(self):
        """
        Animate drawing of cells.
        """

        if self.win:
            self.win.redraw()
            time.sleep(0.01)
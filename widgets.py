from constants import BG_COLOR, FG_COLOR, UNDO_COLOR, ROUTE_COLOR

class Point:
    """
    Represents a point at the end of a line

    :param x: x coordinate of the point
    :type x: int

    :param y: y coordinate of the point
    :type y: int
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    """
    A line, each side ending in a point

    :param point1: A point representing one of the line
    :type point1: widgets.Point

    :param point2: A point representing the other end of the line
    :type point2: widgets.Point
    """

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        """
        Draw the line.

        :param canvas: The canvas
        :type canvas: tkinter.Canvas

        :param fill_color: Color to draw the line as
        :type fill_color: str
        """

        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

class Cell:
    """
    Represents a square cell in the maze

    :param window: The app window
    :type window: tkinter.Tk
    """

    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1

        self.center_x = -1
        self.center_y = -1

        self.__win = window

        self.visited = False
    
    def draw(self, x1, y1, x2, y2):
        """
        Given the coordinates of the cell's corners, set the corner parameters
        and draw the cell.

        :param x1: Left side of the cell
        :type x1: int

        :param y1: Top side of the cell
        :type y1: int

        :param x2: Right side of the cell
        :type x2: int

        :param y2: Bottom side of the cell
        :type y2: int
        """

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        # Calculate the center coordinates of the cell;
        # the move path will connect through the center.
        self.center_x = x1 + ((x2-x1) // 2)
        self.center_y = y1 + ((y2-y1) // 2)

        if self.has_left_wall:
            color = FG_COLOR
        else:
            color = BG_COLOR
        point1 = Point(self.__x1, self.__y1)
        point2 = Point(self.__x1, self.__y2)
        line = Line(point1, point2)
        if self.__win:
            self.__win.draw_line(line, color)

        if self.has_top_wall:
            color = FG_COLOR
        else:
            color = BG_COLOR
        point1 = Point(self.__x1, self.__y1)
        point2 = Point(self.__x2, self.__y1)
        line = Line(point1, point2)
        if self.__win:
            self.__win.draw_line(line, color)


        if self.has_right_wall:
            color = FG_COLOR
        else:
            color = BG_COLOR
        point1 = Point(self.__x2, self.__y1)
        point2 = Point(self.__x2, self.__y2)
        line = Line(point1, point2)
        if self.__win:
            self.__win.draw_line(line, color)

        if self.has_bottom_wall:
            color = FG_COLOR
        else:
            color = BG_COLOR
        point1 = Point(self.__x1, self.__y2)
        point2 = Point(self.__x2, self.__y2)
        line = Line(point1, point2)
        if self.__win:
            self.__win.draw_line(line, color)
    
    def draw_move(self, to_cell, undo=False):
        """
        Draw the move between two cells

        :param to_cell: Destination cell
        :type to_cell: widgets.Cell

        :param undo: Whether this move is an undo.
        If this is an undo, the move will be colored gray.
        Otherwise, the move will be colored red.
        :type undo: bool
        """

        point1 = Point(self.__center_x, self.__center_y)
        point2 = Point(to_cell.__center_x, to_cell.__center_y)
        line = Line(point1, point2)
        
        if undo:
            color = UNDO_COLOR
        else:
            color = ROUTE_COLOR
        
        if self.__win:
            self.__win.draw_line(line, color)

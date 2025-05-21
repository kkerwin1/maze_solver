from tkinter import Tk, BOTH, Canvas
from constants import BG_COLOR

class Window:
    """
    Tk window class.

    :param width: Window width
    :type width: int

    :param height: Window height
    :type height: int
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(
            self.__root, width=self.width, 
            height=self.height, background=BG_COLOR,
        )
        self.__canvas.pack()
        self.running = False

        # Execute self.close() when window close is detected
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """
        Redraw window.
        """

        self.__root.update()
        self.__root.update_idletasks()
    
    def wait_for_close(self):
        """
        Main program loop.
        """

        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        """
        Called when window is closed.
        """

        self.running = False
    
    def draw_line(self, line, fill_color):
        """
        Draw a line.

        :param line: Line object: widgets.Line
        :type line: widgets.Line

        :param fill_color: Color
        :type fill_color: str
        """

        line.draw(self.__canvas, fill_color)
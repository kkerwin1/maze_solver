from gui import Window
from maze import Maze

def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 39, 29, 20, 20, win)
    win.wait_for_close()

if __name__ == "__main__":
    main()

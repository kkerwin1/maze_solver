import unittest

from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_cols, num_rows, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )
    
    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_cols, num_rows, 10, 10)
        enter_cell = m1.cells[0][0]
        exit_cell = m1.cells[len(m1.cells)-1][len(m1.cells[0])-1]
        self.assertEqual(enter_cell.has_top_wall, False)
        self.assertEqual(exit_cell.has_bottom_wall, False)

if __name__ == "__main__":
    unittest.main()
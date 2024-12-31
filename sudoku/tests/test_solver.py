import unittest
from sudoku_solver import sudoku_solver as suso


class TestSolver(unittest.TestCase):

    def test_column_constraint_satisfied(self):
        assignment = {
            0: 1,
            9: 2,
            18: 3,
            27: 4,
            36: 5,
            45: 6,
            54: 7,
            63: 8,
            72: 9
        }

        constraint = suso.ColumnConstraint(0)
        self.assertTrue(constraint.satisfied)

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
        self.assertTrue(constraint.satisfied(assignment))

    def test_column_constraint_satisfied_with_incomplete_column(self):
        assignment = {
            0: 1,
            9: 2,
            18: 3,
            27: 4
        }

        constraint = suso.ColumnConstraint(0)
        self.assertTrue(constraint.satisfied(assignment))

    def test_column_constraint_unsatisfied(self):
        assignment = {
            0: 1,
            9: 2,
            18: 3,
            27: 4,
            36: 5,
            45: 6,
            54: 7,
            63: 8,
            72: 1
        }

        constraint = suso.ColumnConstraint(0)
        self.assertFalse(constraint.satisfied(assignment))

    def test_row_constraint_satisfied(self):
        assignment = {
            0: 1,
            1: 2,
            2: 3,
            3: 4,
            4: 5,
            5: 6,
            6: 7,
            7: 8,
            8: 9
        }

        constraint = suso.RowConstraint(0)
        self.assertTrue(constraint.satisfied(assignment))

    def test_row_constraint_satisfied_with_incomplete_row(self):
        assignment = {
            0: 1,
            1: 2,
            2: 3,
            3: 4,
        }

        constraint = suso.RowConstraint(0)
        self.assertTrue(constraint.satisfied(assignment))

    def test_row_constraint_unsatisfied(self):
        assignment = {
            0: 1,
            1: 2,
            2: 3,
            3: 4,
            4: 5,
            5: 6,
            6: 7,
            7: 8,
            8: 1
        }

        constraint = suso.RowConstraint(0)
        self.assertFalse(constraint.satisfied(assignment))

    def test_sector_constraint_satisfied(self):
        assignment = {
            0: 1,
            1: 2,
            2: 3,
            9: 4,
            10: 5,
            11: 6,
            18: 7,
            19: 8,
            20: 9
        }

        constraint = suso.SectorConstraint(0)
        self.assertTrue(constraint.satisfied(assignment))

    def test_sector_constraint_satisfied_with_incomplete_sector(self):
        assignment = {
            0: 1,
            1: 2,
            2: 3
        }

        constraint = suso.SectorConstraint(0)
        self.assertTrue(constraint.satisfied(assignment))

    def test_sector_constraint_unsatisfied(self):
        assignment = {
            0: 1,
            1: 2,
            2: 3,
            9: 4,
            10: 5,
            11: 6,
            18: 7,
            19: 8,
            20: 1
        }

        constraint = suso.SectorConstraint(0)
        self.assertFalse(constraint.satisfied(assignment))


if __name__ == '__main__':
    unittest.main()

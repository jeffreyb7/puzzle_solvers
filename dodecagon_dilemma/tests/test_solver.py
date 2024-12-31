import unittest
from dodecagon_solver import dodecagon_solver as doso

class TestSolver(unittest.TestCase):

    def setUp(self):
        self.wheel_config: doso.WheelConfiguration = {
            'A': [1, 5, 4, 12, 7, 2, 9, 8, 3, 11, 6, 10],
            'B': [1, 12, 9, 10, 8, 4, 2, 11, 7, 3, 5, 6],
            'C': [1, 6, 7, 10, 4, 2, 11, 3, 12, 9, 8, 3],
            'D': [1, 8, 9, 10, 11, 12, 7, 2, 3, 4, 5, 6],
            'E': [1, 5, 11, 2, 4, 3, 10, 7, 8, 6, 12, 9],
            'F': [1, 10, 11, 3, 4, 8, 9, 2, 6, 5, 7, 12],
            'G': [1, 7, 2, 5, 10, 12, 11, 9, 5, 6, 4, 8],
            'H': [1, 10, 12, 6, 7, 5, 3, 2, 9, 8, 11, 4],
            'I': [1, 7, 5, 3, 12, 10, 11, 9, 2, 6, 4, 8],
            'J': [1, 7, 11, 2, 4, 3, 12, 5, 8, 6, 10, 9],
            'K': [1, 3, 10, 12, 6, 4, 2, 7, 9, 5, 8, 11],
            'L': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        }

    def test_get_wheel_at_nonzero_position(self):
        self.assertEqual(doso.get_wheel_at_position(self.wheel_config, 'F', 4), [6, 5, 7, 12, 1, 10, 11, 3, 4, 8, 9, 2])

    def test_get_wheel_at_zero_position(self):
        self.assertEqual(doso.get_wheel_at_position(self.wheel_config, 'L', 0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    def test_neighbor_constraint_when_satisfied_in_upper_left(self):
        puzzle_state = {
            0: ('A', 0),
            1: ('B', 8),
            4: ('C', 3),
        }
        constraint = doso.NeighborConstraint(0, self.wheel_config)
        self.assertTrue(constraint.satisfied(puzzle_state))
    
    def test_neighbor_constraint_when_unsatisfied_in_upper_left(self):
        puzzle_state = {
            0: ('A', 0),
            1: ('B', 9),
            4: ('C', 4),
        }
        constraint = doso.NeighborConstraint(0, self.wheel_config)
        self.assertFalse(constraint.satisfied(puzzle_state))

    def test_neighbor_constraint_when_satisfied_in_upper_right(self):
        puzzle_state = {
            2: ('B', 8),
            3: ('A', 0),
            7: ('C', 3),
        }
        constraint = doso.NeighborConstraint(3, self.wheel_config)
        self.assertTrue(constraint.satisfied(puzzle_state))

    def test_neighbor_constraint_when_unsatisfied_in_upper_right(self):
        puzzle_state = {
            2: ('B', 9),
            3: ('A', 0),
            7: ('C', 4),
        }
        constraint = doso.NeighborConstraint(3, self.wheel_config)
        self.assertFalse(constraint.satisfied(puzzle_state))

    def test_neighbor_constraint_when_satisfied_in_lower_left(self):
        puzzle_state = {
            4: ('C', 6),
            8: ('A', 0),
            9: ('B', 8),
        }
        constraint = doso.NeighborConstraint(8, self.wheel_config)
        self.assertTrue(constraint.satisfied(puzzle_state))

    def test_neighbor_constraint_when_unsatisfied_in_lower_left(self):
        puzzle_state = {
            4: ('C', 7),
            8: ('A', 0),
            9: ('B', 9),
        }
        constraint = doso.NeighborConstraint(8, self.wheel_config)
        self.assertFalse(constraint.satisfied(puzzle_state))

    def test_neighbor_constraint_when_satisfied_in_lower_right(self):
        puzzle_state = {
            7: ('C', 6),
            10: ('B', 8),
            11: ('A', 0),
        }
        constraint = doso.NeighborConstraint(11, self.wheel_config)
        self.assertTrue(constraint.satisfied(puzzle_state))

    def test_neighbor_constraint_when_unsatisfied_in_lower_right(self):
        puzzle_state = {
            7: ('C', 7),
            10: ('B', 9),
            11: ('A', 0),
        }
        constraint = doso.NeighborConstraint(11, self.wheel_config)
        self.assertFalse(constraint.satisfied(puzzle_state))
    
    def test_neighbor_constraint_when_satisfied_in_middle(self):
        puzzle_state = {
            1: ('C', 6),
            4: ('B', 8),
            5: ('A', 0),
            6: ('D', 4),
            9: ('E', 1)
        }
        constraint = doso.NeighborConstraint(5, self.wheel_config)
        self.assertTrue(constraint.satisfied(puzzle_state))
    
    def test_neighbor_constraint_when_unsatisfied_in_middle(self):
        puzzle_state = {
            1: ('C', 7),
            4: ('B', 9),
            5: ('A', 0),
            6: ('D', 5),
            9: ('E', 2)
        }
        constraint = doso.NeighborConstraint(5, self.wheel_config)
        self.assertFalse(constraint.satisfied(puzzle_state))
    
    # Allows constraint to pass when wheels on the right or below have not been placed yet
    def test_neighbor_constraint_when_satisfied_in_middle_and_ahead_wheels_missing(self):
        puzzle_state = {
            1: ('C', 6),
            4: ('B', 8),
            5: ('A', 0)
        }
        constraint = doso.NeighborConstraint(5, self.wheel_config)
        self.assertTrue(constraint.satisfied(puzzle_state))

if __name__ == '__main__':
    unittest.main()
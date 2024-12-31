from abc import ABC, abstractmethod
import math
from typing import TypeAlias

# Create types for inputs
PuzzleDesign: TypeAlias = list[list[int]]
NumberLocations: TypeAlias = list[int]
NumberChoices: TypeAlias = list[int]

# Base class as a parent of other constraint classes


class Constraint(ABC):

    def __init__(self, position: int):
        self.position = position

    @abstractmethod
    def satisfied(self, assignment: dict[int, int]):
        pass

# Class to check for no duplicate numbers per column


class ColumnConstraint(Constraint):

    def __init__(self, position: int):
        super().__init__(position)

    def satisfied(self, assignment: dict[int, int]) -> bool:
        # Get col number of var
        var_col = self.position % 9
        # List all vars in column
        var_to_check = [x for x in range(var_col, 81, 9)]
        var_values: list[int] = []
        # Check that none of these vars have same assignment
        assigned_vars = list(assignment.keys())
        for position in var_to_check:
            if position in assigned_vars:
                if assignment[position] in var_values:
                    return False
                else:
                    var_values.append(assignment[position])
            else:
                continue

        return True

# Class to check for no duplicate numbers per row


class RowConstraint(Constraint):

    def __init__(self, position: int):
        super().__init__(position)

    def satisfied(self, assignment: dict[int, int]) -> bool:
        # Get row number of var
        var_row = math.floor(self.position / 9)
        # List all vars in row
        var_to_check = [x for x in range(var_row*9, ((var_row+1)*9))]
        var_values: list[int] = []
        # Check that none of these vars have same assignment
        assigned_vars = list(assignment.keys())
        for position in var_to_check:
            if position in assigned_vars:
                if assignment[position] in var_values:
                    return False
                else:
                    var_values.append(assignment[position])
            else:
                continue

        return True

# Class to check for no duplicate numbers per sector


class SectorConstraint(Constraint):

    def __init__(self, position: int):
        super().__init__(position)

    def satisfied(self, assignment: dict[int, int]) -> bool:
        # Get row, col indices of position
        row_idx = math.floor(self.position / 9)
        col_idx = self.position % 9
        # Get sector number of var
        # Sectors are numbered 0 to 8
        # Sector 0 is top left
        # Sector 2 is top right
        # Sector 6 is bottom left
        # Sector 8 is bottom right
        sector_idx = (math.floor(row_idx / 3) * 3) + math.floor(col_idx / 3)
        # Get lowest var number in sector
        lowest_var_id = (math.floor(sector_idx / 3) * 27) + \
            ((sector_idx % 3) * 3)
        # Produce list of the upper 3 positions in the sector
        base_var_to_check = [x for x in range(lowest_var_id, lowest_var_id+3)]
        final_var_to_check: list[int] = []
        # Add all sector positions to list
        for entry in base_var_to_check:
            final_var_to_check.append(entry)
            final_var_to_check.append(entry + 9)
            final_var_to_check.append(entry + 18)
        # Check that none of these vars have same assignment
        var_values: list[int] = []
        assigned_vars = list(assignment.keys())
        for position in final_var_to_check:
            if position in assigned_vars:
                if assignment[position] in var_values:
                    return False
                else:
                    var_values.append(assignment[position])
            else:
                continue

        return True


class CSP:

    def __init__(self, positions: list[int], domains: dict[int, list[int]]):

        self.positions = positions
        self.domains = domains
        self.constraints: dict[int, list[Constraint]] = {}

        for position in self.positions:
            self.constraints[position] = []
            if position not in self.domains:
                raise LookupError(
                    "Every position should have a domain assigned to it")

    # Adds constraints to each position
    def add_constraint(self, constraint: Constraint):

        if constraint.position not in self.positions:
            raise LookupError("Position in constraint not in CSP")
        else:
            self.constraints[position].append(constraint)

    # Checks if all position constraints have been satisfied
    def consistent(self, position: int, assignment: dict[int, int]) -> bool:
        for constraint in self.constraints[position]:
            if not constraint.satisfied(assignment):
                return False
        return True

    # Recursive method responsible for solving the puzzle
    def backtracking_search(self, assignment: dict[int, int]) -> dict[int, int] | None:
        # Check if each position has an assignment. If so, stop
        if len(assignment) == len(self.positions):
            return assignment

        # Get all positions that have not been assigned
        unassigned = [v for v in self.positions if v not in assignment]

        # Get every possible domain value of the first unassigned position
        this_position = unassigned[0]
        for value in self.domains[this_position]:
            local_assignment = assignment.copy()
            local_assignment[this_position] = value
            # Check if constraints are satisfied.
            # If so, continue to recurse
            if self.consistent(this_position, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None


def print_solution(solution: dict[int, int]) -> None:
    solution_keys_sorted = sorted(solution.keys())
    ordered_solution: dict[int, int] = {}
    for key in solution_keys_sorted:
        ordered_solution[key] = solution[key]
    # Create a list of lists for printing
    solution_array: list[list[int]] = []
    row_array: list[int] = []
    for key, value in ordered_solution.items():
        if (key + 1) % 9 == 0:
            row_array.append(value)
            solution_array.append(row_array)
            row_array = []
        else:
            row_array.append(value)
    for row in solution_array:
        for element in row:
            print(element, end=' ')
        print()

    return


if __name__ == "__main__":

    puzzle_design: PuzzleDesign = [
        [2, 0, 0, 0, 8, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 7, 0, 3, 0, 0],
        [0, 3, 0, 8, 4, 0, 0, 0, 6],
        [0, 8, 0, 0, 1, 0, 0, 2, 0],
        [0, 4, 0, 0, 0, 0, 0, 9, 0],
        [1, 0, 0, 0, 0, 7, 0, 0, 9],
        [5, 0, 0, 0, 6, 0, 0, 7, 0],
        [0, 0, 0, 9, 0, 4, 0, 0, 0]
    ]

    """ 
    Answer to the above for verification
    2 5 7 4 8 3 9 6 1 
    3 6 8 5 9 1 7 4 2 
    4 1 9 6 7 2 3 5 8 
    7 3 2 8 4 9 5 1 6 
    9 8 5 7 1 6 4 2 3 
    6 4 1 2 3 5 8 9 7 
    1 2 4 3 5 7 6 8 9 
    5 9 3 1 6 8 2 7 4 
    8 7 6 9 2 4 1 3 5 
    """

    # Initialize positions and domains
    # Position ids are just numbers from 0 to 80
    # Var 0 is upper left of puzzle
    # Var 80 is bottom right of puzzle
    positions: NumberLocations = [x for x in range(0, 81)]
    number_choices: NumberChoices = [x for x in range(1, 10)]
    # Create domains for each position
    domains: dict[int, list[int]] = {}
    for position in positions:
        domains[position] = number_choices

    # Create initial assignment dictionary
    # This maps position to value for the initial state of the puzzle
    assignment: dict[int, int] = {}
    position_id = 0
    for row_idx in range(0, 9):
        for col_idx in range(0, 9):
            if puzzle_design[row_idx][col_idx] != 0:
                assignment[position_id] = puzzle_design[row_idx][col_idx]
                position_id += 1
            else:
                position_id += 1

    # Instantiate CSP class
    csp = CSP(positions, domains)

    # Add constraints
    for position in positions:
        csp.add_constraint(RowConstraint(position))
        csp.add_constraint(ColumnConstraint(position))
        csp.add_constraint(SectorConstraint(position))

    # Get solution
    solution = csp.backtracking_search(assignment)
    if solution is None:
        print('No solution found')
    else:
        print_solution(solution)

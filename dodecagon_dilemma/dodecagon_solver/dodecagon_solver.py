from typing import TypeAlias

# Create types for inputs
WheelChoices: TypeAlias = list[str]
WheelOrientations: TypeAlias = list[int]
WheelLocations: TypeAlias = list[int]
WheelConfiguration: TypeAlias = dict

# Rotates wheels and returns contents of the wheel in the new order


def get_wheel_at_position(wheel_config: dict, wheel_id: str, position: int) -> list[int]:
    wheel_ids = []
    for id in wheel_config:
        wheel_ids.append(id)
    wheel_size = len(wheel_config[wheel_ids[0]])

    if position == 0:
        return wheel_config[wheel_id]
    else:
        rotated = []
        for idx in range(wheel_size - position, wheel_size):
            rotated.append(wheel_config[wheel_id][idx])
        for idx in range(0, wheel_size - position):
            rotated.append(wheel_config[wheel_id][idx])

        return rotated

# Base class as a parent of other constraint classes


class Constraint:

    def __init__(self, position: int):
        self.position = position

    def satisfied(self, assignment: dict):
        pass

# Class to check that a single wheel is in parity with its neighbors


class NeighborConstraint(Constraint):

    def __init__(self, position: int, wheel_config: dict):
        super().__init__(position)
        self.wheel_config = wheel_config

    # Assignment is the current puzzle configuration
    # Wheel_config is the order of numbers on each wheel at position 0
    def satisfied(self, assignment: dict) -> bool:
        # Identify where neighbors are
        neighbors = {
            'Up': None,
            'Dn': None,
            'Lt': None,
            'Rt': None
        }
        # Identify location of wheel above, if it exists
        if self.position >= 4 and self.position <= 11:
            neighbors['Up'] = self.position - 4
        # Identify location of wheel below, if it exists and has been assigned
        if self.position >= 0 and self.position <= 7:
            if self.position + 4 in assignment:
                if assignment[self.position + 4] is not None:
                    neighbors['Dn'] = self.position + 4
        # Identify location of wheel to the left, if it exists
        if self.position not in [0, 4, 8]:
            neighbors['Lt'] = self.position - 1
        # Identify location of wheel to the right, if it exists and has been assigned
        if self.position not in [3, 7, 11]:
            if self.position + 1 in assignment:
                if assignment[self.position + 1] is not None:
                    neighbors['Rt'] = self.position + 1

        # Get orientation of the current wheel
        current_config = get_wheel_at_position(
            self.wheel_config, assignment[self.position][0], assignment[self.position][1])
        # Check above
        if neighbors['Up'] is not None:
            up_config = get_wheel_at_position(
                self.wheel_config, assignment[neighbors['Up']][0], assignment[neighbors['Up']][1])
            if up_config[6] != current_config[0]:
                return False
        # Check below
        if neighbors['Dn'] is not None:
            dn_config = get_wheel_at_position(
                self.wheel_config, assignment[neighbors['Dn']][0], assignment[neighbors['Dn']][1])
            if dn_config[0] != current_config[6]:
                return False
        # Check left
        if neighbors['Lt'] is not None:
            lt_config = get_wheel_at_position(
                self.wheel_config, assignment[neighbors['Lt']][0], assignment[neighbors['Lt']][1])
            if lt_config[3] != current_config[9]:
                return False
        # Check right
        if neighbors['Rt'] is not None:
            rt_config = get_wheel_at_position(
                self.wheel_config, assignment[neighbors['Rt']][0], assignment[neighbors['Rt']][1])
            if rt_config[9] != current_config[3]:
                return False

        return True


class CSP:

    def __init__(self, positions: list[int], domains: dict):

        self.positions = positions
        self.domains = domains
        self.constraints = {}

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
            self.constraints[constraint.position].append(constraint)

    # Checks if all position constraints have been satisfied
    def consistent(self, position: int, assignment: dict) -> bool:
        for constraint in self.constraints[position]:
            if not constraint.satisfied(assignment):
                return False
        return True

    # Recursive method responsible for solving the puzzle
    def backtracking_search(self, assignment: dict) -> dict | None:
        # Check if each position has an assignment. If so, stop
        if len(assignment) == len(self.positions):
            return assignment

        # Get all positions that have not been assigned
        unassigned = [v for v in self.positions if v not in assignment]
        # Get wheel id's that are still available
        used_wheels = []
        for item in assignment.values():
            used_wheels.append(item[0])
        unused_wheels = [w for w in self.domains[0][0] if w not in used_wheels]

        # Get every possible domain value of the first unassigned position
        first_var = unassigned[0]
        for wheel_choice in unused_wheels:
            if wheel_choice in assignment:
                continue
            for wheel_config in self.domains[first_var][1]:
                local_assignment = assignment.copy()
                local_assignment[first_var] = (wheel_choice, wheel_config)
                # Check if constraints are satisfied.
                # If so, continue to recurse
                if self.consistent(first_var, local_assignment):
                    result = self.backtracking_search(local_assignment)
                    if result is not None:
                        return result
        return None

# Solution is the same structure as assignment


def print_solution(solution: dict) -> None:
    print(f'   {get_wheel_at_position(wheel_config, solution[0][0], solution[0][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[1][0], solution[1][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[2][0], solution[2][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[3][0], solution[3][1])[0]:>2}')

    print(f'{get_wheel_at_position(wheel_config, solution[0][0], solution[0][1])[9]:>2}',
          f' {solution[0][0]}',
          f' {get_wheel_at_position(wheel_config, solution[0][0], solution[0][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[1][0], solution[1][1])[9]:>2}',
          f' {solution[1][0]}',
          f' {get_wheel_at_position(wheel_config, solution[1][0], solution[1][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[2][0], solution[2][1])[9]:>2}',
          f' {solution[2][0]}',
          f' {get_wheel_at_position(wheel_config, solution[2][0], solution[2][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[3][0], solution[3][1])[9]:>2}',
          f' {solution[3][0]}',
          f' {get_wheel_at_position(wheel_config, solution[3][0], solution[3][1])[3]:>2}')

    print(f'   {get_wheel_at_position(wheel_config, solution[0][0], solution[0][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[1][0], solution[1][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[2][0], solution[2][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[3][0], solution[3][1])[6]:>2}')

    print(f'   {get_wheel_at_position(wheel_config, solution[4][0], solution[4][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[5][0], solution[5][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[6][0], solution[6][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[7][0], solution[7][1])[0]:>2}')

    print(f'{get_wheel_at_position(wheel_config, solution[4][0], solution[4][1])[9]:>2}',
          f' {solution[4][0]}',
          f' {get_wheel_at_position(wheel_config, solution[4][0], solution[4][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[5][0], solution[5][1])[9]:>2}',
          f' {solution[5][0]}',
          f' {get_wheel_at_position(wheel_config, solution[5][0], solution[5][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[6][0], solution[6][1])[9]:>2}',
          f' {solution[6][0]}',
          f' {get_wheel_at_position(wheel_config, solution[6][0], solution[6][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[7][0], solution[7][1])[9]:>2}',
          f' {solution[7][0]}',
          f' {get_wheel_at_position(wheel_config, solution[7][0], solution[7][1])[3]:>2}')

    print(f'   {get_wheel_at_position(wheel_config, solution[4][0], solution[4][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[5][0], solution[5][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[6][0], solution[6][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[7][0], solution[7][1])[6]:>2}')

    print(f'   {get_wheel_at_position(wheel_config, solution[8][0], solution[8][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[9][0], solution[9][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[10][0], solution[10][1])[0]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[11][0], solution[11][1])[0]:>2}')

    print(f'{get_wheel_at_position(wheel_config, solution[8][0], solution[8][1])[9]:>2}',
          f' {solution[8][0]}',
          f' {get_wheel_at_position(wheel_config, solution[8][0], solution[8][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[9][0], solution[9][1])[9]:>2}',
          f' {solution[9][0]}',
          f' {get_wheel_at_position(wheel_config, solution[9][0], solution[9][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[10][0], solution[10][1])[9]:>2}',
          f' {solution[10][0]}',
          f' {get_wheel_at_position(wheel_config, solution[10][0], solution[10][1])[3]:>2}',
          f'{get_wheel_at_position(wheel_config, solution[11][0], solution[11][1])[9]:>2}',
          f' {solution[11][0]}',
          f' {get_wheel_at_position(wheel_config, solution[11][0], solution[11][1])[3]:>2}')

    print(f'   {get_wheel_at_position(wheel_config, solution[8][0], solution[8][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[9][0], solution[9][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[10][0], solution[10][1])[6]:>2}',
          f'       {get_wheel_at_position(wheel_config, solution[11][0], solution[11][1])[6]:>2}')

    return


if __name__ == "__main__":

    # Initialize wheel positions
    # Wheel_choice indicates which wheel is chosen
    # Wheel_config indicates the orientation of the wheel
    # Wheel_location indicates the location where a wheel is placed
    # Wheel_contents refers to the order of numbers on a wheel, going clockwise. Position 0 is at 12 o'clock
    wheel_choices: WheelChoices = ['A', 'B', 'C',
                                   'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    wheel_orientations: WheelOrientations = [x for x in range(0, 12)]
    wheel_locations: WheelLocations = [x for x in range(0, 12)]
    wheel_config: WheelConfiguration = {
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

    # Create domains for each position
    # The domain refers to all the possibilities that a given location on the board can have
    domains = {}
    for location in wheel_locations:
        domains[location] = [wheel_choices, wheel_orientations]

    # Assignment tracks the current state of the board as the puzzle is being solved
    # Keys are the same as wheel_locations
    # Values are a tuple of (wheel_choice, wheel_orientation)
    assignment = {}

    # Instantiate CSP class
    csp = CSP(wheel_locations, domains)

    # Add constraints
    for location in wheel_locations:
        csp.add_constraint(NeighborConstraint(location, wheel_config))

    # Get solution
    solution = csp.backtracking_search(assignment)
    if solution is None:
        print('No solution found')
    else:
        print_solution(solution)

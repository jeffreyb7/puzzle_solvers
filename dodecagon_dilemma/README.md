# Dodecagon Dilemma Puzzle

## Components
### CSP class (for Constraint Satisfaction Problem)
- Contains:
    - Positions, a list of the positions in the puzzle
      - Here it is 0 to 11 indicating the wheel locations
      - 0 to 3 is the first row (left to right)
      - 4 to 7 is the second row
      - 8 to 11 is the third row
    - Domains, a dictionary mapping each position (key) to its possible values
      - Possible values in this case are a combination of a wheel and an orientation
      - Therefore each value is an array where:
        - The first member is a list of all the wheel choices
        - The second member is a list of all wheel orientations (list of 0 to 11)
            - Wheel orientation is relative to where the 1 is on each wheel
            - Orientation 0 means the 1 points to 12 o'clock
            - Orientation 3 means the 1 points to 3 o'clock
            - The orientation increases from 0 to 11 in a clockwise motion
    - Constraints, a dictionary mapping each position (key) to a list of its constraints
      - Each constraint is a class object.
    - In this case, each position has one constraint (NeighborConstraint), dictating that it must match the numbers of its neighbors at the touch points

### Assignment 
- A dictionary mapping each position (key) to its assigned configuration
- The value is a tuple where:
    - The first member indicates the wheel id (A through L) chosen for the location
    - The second member indicates the wheel orientation (0 through 11)
- At the start, the assignment is empty, as no configuration has been chosen yet

#### Take a look at the unit tests to get a better idea of how the data structures look

## The solution process
- The assignment is passed into the recursive backtracking search, which:
    - Checks if each position has been assigned a value (solution is found)
    - Creates a list of positions that have not been assigned a value
    - Creates a list of wheel id's that have not been used yet
    - Makes a copy of the assignment dictionary called local assignment
    - Takes the first unassigned position, assigns the first combination of wheel id x orientation, and enters it into local assignment
    - Checks that all constraints are satisfied
    - If so, calls the backtracking search again
    - Once a constraint fails, it returns None
    - None propagates back up the recursive chain until a valid state is reached
    - Continues with the next options from that valid state
    - Repeats until a solution is reached or no solution exists
# Sudoku Puzzle

## Components
### CSP class (for Constraint Satisfaction Problem)
- Contains:
    - Positions, a list of the positions in the puzzle
      - Here it is 0 to 80 indicating the number locations
      - 0 to 8 is the first row (left to right)
      - 9 to 17 is the second row, etc
    - Domains, a dictionary mapping each position (key) to its possible values
      - Possible values in this case are integers 1 through 9
    - Constraints, a dictionary mapping each position (key) to a list of its constraints
      - Each constraint is a class object.
    - In this case, each position has three constraints:
      - A column constraint, dictating that a number must be unique in its own column
      - A row constraint, dictating that a number must be unique in its own row
      - A sector constraint, dictating that a number must be unique in its own sector
        - Sector refers to the 3 x 3 squares on the sudoku board

### Assignment 
- A dictionary mapping each position (key) to its assigned number
- At the start, the assignment represents the given layout of numbers on the board

#### Take a look at the unit tests to get a better idea of how the data structures look

## The solution process
- The assignment is passed into the recursive backtracking search, which:
    - Checks if each position has been assigned a value (solution is found)
    - Creates a list of positions that have not been assigned a value
    - Makes a copy of the assignment dictionary called local assignment
    - Takes the first unassigned position, assigns the first number in the domain list, and enters it into local assignment
    - Checks that all constraints are satisfied
    - If so, calls the backtracking search again
    - Once a constraint fails, it returns None
    - None propagates back up the recursive chain until a valid state is reached
    - Continues with the next options from that valid state
    - Repeats until a solution is reached or no solution exists
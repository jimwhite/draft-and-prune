from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["bluejay", "falcon", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The falcon is to the left of the blue jay: falcon < bluejay
problem.addConstraint(lambda falcon, bluejay: falcon < bluejay, ("falcon", "bluejay"))

# The falcon is to the right of the raven: raven < falcon
problem.addConstraint(lambda raven, falcon: raven < falcon, ("raven", "falcon"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which bird is leftmost (position 1)
leftmost_bird = None
for solution in solutions:
    for bird, pos in solution.items():
        if pos == 1:
            leftmost_bird = bird
            break

# Map to the correct choice letter
if leftmost_bird == "raven":
    print("C")
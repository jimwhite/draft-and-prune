from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three birds
birds = ["bluejay", "falcon", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The falcon is to the left of the blue jay" → falcon < bluejay
problem.addConstraint(lambda falcon, bluejay: falcon < bluejay, ("falcon", "bluejay"))

# "The falcon is to the right of the raven" → raven < falcon
problem.addConstraint(lambda raven, falcon: raven < falcon, ("raven", "falcon"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "bluejay",
    "B": "falcon",
    "C": "raven"
}

# Find which bird is leftmost (position 1)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)
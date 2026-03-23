from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["blue jay", "falcon", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The falcon is to the left of the blue jay" => falcon < blue jay
problem.addConstraint(lambda falcon, blue_jay: falcon < blue_jay, ["falcon", "blue jay"])

# "The falcon is to the right of the raven" => raven < falcon
problem.addConstraint(lambda raven, falcon: raven < falcon, ["raven", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue jay",
    "B": "falcon",
    "C": "raven"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)
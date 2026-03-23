from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["crow", "falcon", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The crow is to the left of the raven" → crow < raven
problem.addConstraint(lambda crow, raven: crow < raven, ["crow", "raven"])

# 3. "The falcon is to the right of the raven" → raven < falcon
problem.addConstraint(lambda raven, falcon: raven < falcon, ["raven", "falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "raven"
}

# Find which bird is in position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)
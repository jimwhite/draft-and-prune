from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["crow", "falcon", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The crow is to the left of the raven"
problem.addConstraint(lambda crow, raven: crow < raven, ["crow", "raven"])

# "The falcon is to the right of the raven"
problem.addConstraint(lambda raven, falcon: raven < falcon, ["raven", "falcon"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which bird is second from the left (position 2)
choices = {
    "A": "crow",
    "B": "falcon",
    "C": "raven"
}

# Find and print the correct choice
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)
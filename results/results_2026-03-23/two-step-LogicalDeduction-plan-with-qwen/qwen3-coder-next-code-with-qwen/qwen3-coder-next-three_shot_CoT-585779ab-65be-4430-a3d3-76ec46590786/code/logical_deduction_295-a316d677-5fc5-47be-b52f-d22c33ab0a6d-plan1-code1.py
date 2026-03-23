from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
birds = ["hawk", "crow", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the right of the hawk"
problem.addConstraint(lambda hawk, raven: hawk < raven, ["hawk", "raven"])

# "The crow is the rightmost"
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "hawk",
    "B": "crow",
    "C": "raven"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)
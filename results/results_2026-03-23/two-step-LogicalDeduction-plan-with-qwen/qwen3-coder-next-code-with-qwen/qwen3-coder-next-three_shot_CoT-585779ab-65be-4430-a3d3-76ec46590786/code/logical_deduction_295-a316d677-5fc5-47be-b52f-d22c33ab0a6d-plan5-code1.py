from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["hawk", "crow", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the right of the hawk" -> hawk < raven
problem.addConstraint(lambda hawk, raven: hawk < raven, ["hawk", "raven"])

# "The crow is the rightmost" -> crow == 3
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which bird is leftmost (position 1)
choices = {
    "A": "hawk",
    "B": "crow",
    "C": "raven"
}

# Find the bird at position 1 and print its corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)
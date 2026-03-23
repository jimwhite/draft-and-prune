from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["falcon", "owl", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the left of the owl"
problem.addConstraint(lambda raven, owl: raven < owl, ["raven", "owl"])

# "The falcon is the leftmost"
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "falcon",
    "B": "owl",
    "C": "raven"
}

# Find the bird at position 3 (rightmost) and print corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)
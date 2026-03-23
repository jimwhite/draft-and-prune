from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["raven", "quail", "crow"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The quail is the leftmost (position 1)
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# The raven is the rightmost (position 3)
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "raven",
    "B": "quail",
    "C": "crow"
}

# Find which bird is at position 3 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)
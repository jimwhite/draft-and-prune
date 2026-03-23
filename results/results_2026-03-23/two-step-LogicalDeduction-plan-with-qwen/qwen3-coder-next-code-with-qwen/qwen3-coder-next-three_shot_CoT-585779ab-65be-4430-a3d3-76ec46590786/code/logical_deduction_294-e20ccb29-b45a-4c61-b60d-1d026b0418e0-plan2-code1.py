from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["raven", "quail", "crow"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The quail is the leftmost (position 1)
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# The raven is the rightmost (position 3)
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "raven",
    "B": "quail",
    "C": "crow"
}

# Find which bird is at position 3 (rightmost) and print the corresponding letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)
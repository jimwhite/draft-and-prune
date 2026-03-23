from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["crow", "robin", "quail", "bluejay", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The robin is to the left of the quail"
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# "The falcon is the third from the left"
problem.addConstraint(lambda falcon: falcon == 3, ["falcon"])

# "The crow is to the left of the falcon"
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# "The blue jay is the leftmost"
problem.addConstraint(lambda bluejay: bluejay == 1, ["bluejay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "crow",
    "B": "robin",
    "C": "quail",
    "D": "bluejay",
    "E": "falcon"
}

# Find which bird is in position 3 (third from left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5)
birds = ["bluejay", "raven", "crow", "falcon", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The crow is to the left of the quail"
problem.addConstraint(lambda crow, quail: crow < quail, ("crow", "quail"))

# "The falcon is the leftmost"
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# "The blue jay is to the right of the quail"
problem.addConstraint(lambda bluejay, quail: bluejay > quail, ("bluejay", "quail"))

# "The raven is the second from the left"
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds
choices = {
    "A": "bluejay",
    "B": "raven",
    "C": "crow",
    "D": "falcon",
    "E": "quail"
}

# Find which bird is at position 5 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)
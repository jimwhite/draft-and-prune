from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds)
birds = ["blue jay", "raven", "crow", "falcon", "quail"]

# Define domain (positions 1 to 5, where 1 is leftmost and 5 is rightmost)
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The falcon is the leftmost" → falcon == 1
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# "The raven is the second from the left" → raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# "The crow is to the left of the quail" → crow < quail
problem.addConstraint(lambda crow, quail: crow < quail, ["crow", "quail"])

# "The blue jay is to the right of the quail" → quail < blue_jay
problem.addConstraint(lambda quail, blue_jay: quail < blue_jay, ["quail", "blue jay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "blue jay",
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
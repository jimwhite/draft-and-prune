from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["blue jay", "raven", "crow", "falcon", "quail"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The crow is to the left of the quail" -> crow < quail
problem.addConstraint(lambda crow, quail: crow < quail, ["crow", "quail"])

# "The falcon is the leftmost" -> falcon == 1
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# "The blue jay is to the right of the quail" -> blue jay > quail
problem.addConstraint(lambda blue_jay, quail: blue_jay > quail, ["blue jay", "quail"])

# "The raven is the second from the left" -> raven == 2
problem.addConstraint(lambda raven: raven == 2, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to bird names
choices = {
    "A": "blue jay",
    "B": "raven",
    "C": "crow",
    "D": "falcon",
    "E": "quail"
}

# Find which bird is at position 2 (second from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 2:
            print(letter)
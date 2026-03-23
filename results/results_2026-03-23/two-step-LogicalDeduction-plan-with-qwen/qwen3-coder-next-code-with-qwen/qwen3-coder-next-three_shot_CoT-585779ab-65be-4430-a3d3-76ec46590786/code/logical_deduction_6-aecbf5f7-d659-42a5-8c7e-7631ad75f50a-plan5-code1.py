from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (birds) and domain (positions 1 to 5, where 1 is leftmost)
birds = ["crow", "robin", "quail", "bluejay", "falcon"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The robin is to the left of the quail"
problem.addConstraint(lambda robin, quail: robin < quail, ["robin", "quail"])

# 3. "The falcon is the third from the left"
problem.addConstraint(lambda falcon: falcon == 3, ["falcon"])

# 4. "The crow is to the left of the falcon"
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# 5. "The blue jay is the leftmost"
problem.addConstraint(lambda bluejay: bluejay == 1, ["bluejay"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names as per the choices
choices = {
    "A": "crow",
    "B": "robin",
    "C": "quail",
    "D": "bluejay",
    "E": "falcon"
}

# Find which bird is at position 3 (third from the left)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)
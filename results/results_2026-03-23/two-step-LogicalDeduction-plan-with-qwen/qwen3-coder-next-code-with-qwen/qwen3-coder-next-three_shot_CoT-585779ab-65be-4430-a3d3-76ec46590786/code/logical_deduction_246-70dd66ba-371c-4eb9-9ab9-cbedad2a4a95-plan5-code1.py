from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["owl", "crow", "cardinal"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The crow is to the left of the owl." -> crow < owl
problem.addConstraint(lambda crow, owl: crow < owl, ["crow", "owl"])

# 3. "The owl is the second from the left." -> owl == 2
problem.addConstraint(lambda owl: owl == 2, ["owl"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to birds for the rightmost position (position 3)
choices = {
    "A": "owl",
    "B": "crow",
    "C": "cardinal"
}

# Find which bird is at position 3 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 3:
            print(letter)
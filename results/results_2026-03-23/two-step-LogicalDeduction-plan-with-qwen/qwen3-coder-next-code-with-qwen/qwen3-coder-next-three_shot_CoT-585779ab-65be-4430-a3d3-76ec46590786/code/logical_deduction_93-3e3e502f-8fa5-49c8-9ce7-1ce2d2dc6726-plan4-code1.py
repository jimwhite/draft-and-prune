from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints based on the problem description
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The raven is to the left of the hummingbird."
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ["raven", "hummingbird"])

# 3. "The hawk is to the left of the owl."
problem.addConstraint(lambda hawk, owl: hawk < owl, ["hawk", "owl"])

# 4. "The cardinal is to the left of the hawk."
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# 5. "The raven is the second from the right." (position 4 in a 1-5 scale)
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names for the rightmost position (position 5)
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird",
    "D": "raven",
    "E": "owl"
}

# Find which bird is at position 5 (rightmost) and print the corresponding choice letter
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)
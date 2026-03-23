from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds) and domain (positions 1 to 5)
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]
positions = range(1, 6)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the left of the hummingbird"
problem.addConstraint(lambda raven, hummingbird: raven < hummingbird, ["raven", "hummingbird"])

# "The hawk is to the left of the owl"
problem.addConstraint(lambda hawk, owl: hawk < owl, ["hawk", "owl"])

# "The cardinal is to the left of the hawk"
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ["cardinal", "hawk"])

# "The raven is the second from the right" (position 4 in a 5-position sequence)
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to bird names
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird",
    "D": "raven",
    "E": "owl"
}

# Find which bird is at position 1 (leftmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 1:
            print(letter)
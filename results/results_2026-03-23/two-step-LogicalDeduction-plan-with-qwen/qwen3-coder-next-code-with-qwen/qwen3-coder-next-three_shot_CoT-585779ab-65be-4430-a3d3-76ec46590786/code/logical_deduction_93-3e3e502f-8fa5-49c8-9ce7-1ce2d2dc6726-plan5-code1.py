from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the five birds)
birds = ["cardinal", "hawk", "hummingbird", "raven", "owl"]

# Define domain (positions 1 to 5, where 1 = leftmost, 5 = rightmost)
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

# "The raven is the second from the right" (position 4)
problem.addConstraint(lambda raven: raven == 4, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to birds
choices = {
    "A": "cardinal",
    "B": "hawk",
    "C": "hummingbird",
    "D": "raven",
    "E": "owl"
}

# Find which bird is at position 5 (rightmost)
for solution in solutions:
    for letter, bird_name in choices.items():
        if solution[bird_name] == 5:
            print(letter)
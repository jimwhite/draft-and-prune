from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
birds = ["falcon", "owl", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The raven is to the left of the owl"
problem.addConstraint(lambda raven, owl: raven < owl, ["raven", "owl"])

# "The falcon is the leftmost"
problem.addConstraint(lambda falcon: falcon == 1, ["falcon"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which bird is rightmost (position 3)
for solution in solutions:
    if solution["falcon"] == 3:
        print("A")
    elif solution["owl"] == 3:
        print("B")
    elif solution["raven"] == 3:
        print("C")
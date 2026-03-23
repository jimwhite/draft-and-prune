from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three birds
birds = ["cardinal", "hawk", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# "The hummingbird is to the right of the hawk" -> hummingbird > hawk
problem.addConstraint(lambda hawk, hummingbird: hummingbird > hawk, ("hawk", "hummingbird"))

# "The cardinal is to the left of the hawk" -> cardinal < hawk
problem.addConstraint(lambda cardinal, hawk: cardinal < hawk, ("cardinal", "hawk"))

# Solve the problem
solutions = problem.getSolutions()

# Find which bird is leftmost (position 1) and map to choice letter
for solution in solutions:
    if solution["cardinal"] == 1:
        print("A")
    elif solution["hawk"] == 1:
        print("B")
    elif solution["hummingbird"] == 1:
        print("C")
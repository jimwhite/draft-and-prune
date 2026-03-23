from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["raven", "quail", "crow"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
# All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# The quail is the leftmost (position 1)
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# The raven is the rightmost (position 3)
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which bird is rightmost (position 3)
for solution in solutions:
    if solution["raven"] == 3:
        print("A")
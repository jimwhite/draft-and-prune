from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["raven", "quail", "crow"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The quail is the leftmost"
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# "The raven is the rightmost"
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which bird is at position 3 (rightmost)
for solution in solutions:
    if solution["raven"] == 3:
        print("A")
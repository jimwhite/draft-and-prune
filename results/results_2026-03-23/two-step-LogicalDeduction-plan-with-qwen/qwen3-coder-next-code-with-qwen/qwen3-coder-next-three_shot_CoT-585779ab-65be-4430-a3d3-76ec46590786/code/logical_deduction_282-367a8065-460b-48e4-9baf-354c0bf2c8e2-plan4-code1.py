from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["quail", "owl", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The quail is to the left of the owl
problem.addConstraint(lambda quail, owl: quail < owl, ["quail", "owl"])

# The owl is to the left of the hummingbird
problem.addConstraint(lambda owl, hummingbird: owl < hummingbird, ["owl", "hummingbird"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which bird is rightmost (position 3)
for solution in solutions:
    if solution["hummingbird"] == 3:
        print("C")
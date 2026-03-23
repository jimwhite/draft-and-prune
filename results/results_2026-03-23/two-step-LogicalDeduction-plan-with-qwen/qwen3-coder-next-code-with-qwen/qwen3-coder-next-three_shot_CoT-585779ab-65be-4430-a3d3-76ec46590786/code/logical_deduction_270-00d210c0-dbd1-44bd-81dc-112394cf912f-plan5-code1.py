from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
birds = ["crow", "falcon", "hummingbird"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# The crow is to the left of the falcon: crow < falcon
problem.addConstraint(lambda crow, falcon: crow < falcon, ["crow", "falcon"])

# The hummingbird is to the left of the crow: hummingbird < crow
problem.addConstraint(lambda hummingbird, crow: hummingbird < crow, ["hummingbird", "crow"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which bird is rightmost (position 3)
for solution in solutions:
    if solution["falcon"] == 3:
        print("B")
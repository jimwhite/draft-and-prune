from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain for three birds
birds = ["hawk", "crow", "raven"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The raven is to the right of the hawk" -> raven > hawk
problem.addConstraint(lambda hawk, raven: raven > hawk, ["hawk", "raven"])

# 3. "The crow is the rightmost" -> crow == 3
problem.addConstraint(lambda crow: crow == 3, ["crow"])

# Solve the problem
solutions = problem.getSolutions()

# Get the first (and only) solution
solution = solutions[0]

# Check which bird is leftmost (position 1)
if solution["hawk"] == 1:
    print("A")
elif solution["crow"] == 1:
    print("B")
elif solution["raven"] == 1:
    print("C")
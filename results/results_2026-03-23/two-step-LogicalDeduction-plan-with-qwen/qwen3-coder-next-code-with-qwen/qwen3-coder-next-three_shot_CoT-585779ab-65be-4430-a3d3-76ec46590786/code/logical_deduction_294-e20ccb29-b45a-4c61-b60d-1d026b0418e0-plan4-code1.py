from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the three birds) and domain (positions 1 to 3)
birds = ["raven", "quail", "crow"]
positions = range(1, 4)
problem.addVariables(birds, positions)

# Add constraints based on the statements
# 1. All birds must be in different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The quail is the leftmost." (position 1)
problem.addConstraint(lambda quail: quail == 1, ["quail"])

# 3. "The raven is the rightmost." (position 3)
problem.addConstraint(lambda raven: raven == 3, ["raven"])

# Solve the problem
solutions = problem.getSolutions()

# Check which choice is true based on the solution
for solution in solutions:
    # According to the constraints, we know:
    # quail = 1 (leftmost), raven = 3 (rightmost), so crow must be at position 2
    # Now verify the choices:
    if solution["raven"] == 3:
        print("A")
    elif solution["quail"] == 3:
        print("B")
    elif solution["crow"] == 3:
        print("C")
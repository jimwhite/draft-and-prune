from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 3)
golfers = ["mel", "ada", "ana"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different positions
problem.addConstraint(AllDifferentConstraint())

# Mel finished last (position 3)
problem.addConstraint(lambda mel: mel == 3, ["mel"])

# Ana finished second (position 2)
problem.addConstraint(lambda ana: ana == 2, ["ana"])

# Solve the problem
solutions = problem.getSolutions()

# Determine who finished second (position 2)
for solution in solutions:
    if solution["mel"] == 3 and solution["ana"] == 2:
        # Ada must be in position 1, but we only need to check who is second
        if solution["ada"] == 2:
            print("B")
        elif solution["ana"] == 2:
            print("C")
        break
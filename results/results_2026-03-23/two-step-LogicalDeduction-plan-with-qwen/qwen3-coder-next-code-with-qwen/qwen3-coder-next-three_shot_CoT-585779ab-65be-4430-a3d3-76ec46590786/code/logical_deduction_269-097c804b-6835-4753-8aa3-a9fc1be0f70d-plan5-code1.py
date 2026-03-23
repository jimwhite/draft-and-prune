from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=last)
golfers = ["mel", "ada", "ana"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraint that all golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Mel finished last" → mel = 3
problem.addConstraint(lambda mel: mel == 3, ["mel"])

# "Ana finished second" → ana = 2
problem.addConstraint(lambda ana: ana == 2, ["ana"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which choice is true based on the solution
for solution in solutions:
    # Check each choice
    if solution["mel"] == 2:  # Choice A
        print("A")
    elif solution["ada"] == 2:  # Choice B
        print("B")
    elif solution["ana"] == 2:  # Choice C
        print("C")
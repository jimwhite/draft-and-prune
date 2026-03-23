from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["Dan", "Mel", "Amy"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Dan finished above Amy" → Dan's position < Amy's position
problem.addConstraint(lambda d, a: d < a, ("Dan", "Amy"))

# "Amy finished above Mel" → Amy's position < Mel's position
problem.addConstraint(lambda a, m: a < m, ("Amy", "Mel"))

# Solve the problem
solutions = problem.getSolutions()

# Determine who finished first (position 1) and map to the correct choice
for solution in solutions:
    if solution["Dan"] == 1:
        print("A")
    elif solution["Mel"] == 1:
        print("B")
    elif solution["Amy"] == 1:
        print("C")
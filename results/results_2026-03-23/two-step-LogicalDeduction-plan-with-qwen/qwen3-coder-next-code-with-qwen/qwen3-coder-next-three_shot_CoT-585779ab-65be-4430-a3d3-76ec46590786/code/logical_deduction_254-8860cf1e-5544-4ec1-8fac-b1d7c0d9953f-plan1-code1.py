from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["Ana", "Dan", "Mel"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished second
problem.addConstraint(lambda Dan: Dan == 2, ["Dan"])

# Mel finished first
problem.addConstraint(lambda Mel: Mel == 1, ["Mel"])

# Solve the problem
solutions = problem.getSolutions()

# Determine the correct answer based on who finished first
for solution in solutions:
    if solution["Mel"] == 1:
        print("C")
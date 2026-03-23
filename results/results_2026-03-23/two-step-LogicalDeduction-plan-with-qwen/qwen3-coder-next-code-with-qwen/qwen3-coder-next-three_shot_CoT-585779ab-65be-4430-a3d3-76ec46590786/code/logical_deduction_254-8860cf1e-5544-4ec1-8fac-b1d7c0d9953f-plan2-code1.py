from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Ana", "Dan", "Mel"]
ranks = range(1, 4)  # 1=first, 2=second, 3=third
problem.addVariables(golfers, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Dan finished second
problem.addConstraint(lambda Dan: Dan == 2, ["Dan"])

# Mel finished first
problem.addConstraint(lambda Mel: Mel == 1, ["Mel"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which choice is true based on the solution
for solution in solutions:
    # Check each choice
    if solution["Mel"] == 1:
        print("C")
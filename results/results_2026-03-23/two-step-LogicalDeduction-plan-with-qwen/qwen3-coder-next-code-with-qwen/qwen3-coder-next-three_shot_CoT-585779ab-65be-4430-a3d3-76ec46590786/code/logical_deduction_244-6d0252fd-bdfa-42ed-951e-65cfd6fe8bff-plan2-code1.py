from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "convertible", "minivan"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is the second-newest" means rank 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# "The minivan is newer than the convertible" means minivan > convertible
problem.addConstraint(lambda convertible, minivan: convertible < minivan, ["convertible", "minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which vehicle is oldest (rank 1)
for solution in solutions:
    if solution["convertible"] == 1:
        print("B")
    elif solution["tractor"] == 1:
        print("A")
    elif solution["minivan"] == 1:
        print("C")
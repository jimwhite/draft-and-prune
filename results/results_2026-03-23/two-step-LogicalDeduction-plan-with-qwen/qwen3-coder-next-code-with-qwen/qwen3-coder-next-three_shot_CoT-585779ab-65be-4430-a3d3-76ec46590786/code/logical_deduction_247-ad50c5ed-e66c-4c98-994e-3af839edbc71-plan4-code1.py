from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["truck", "minivan", "tractor"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The truck is newer than the minivan" → truck > minivan
problem.addConstraint(lambda truck, minivan: truck > minivan, ("truck", "minivan"))

# "The minivan is newer than the tractor" → minivan > tractor
problem.addConstraint(lambda minivan, tractor: minivan > tractor, ("minivan", "tractor"))

# Solve the problem
solutions = problem.getSolutions()

# Find which vehicle is the oldest (rank 1)
for solution in solutions:
    for vehicle, rank in solution.items():
        if rank == 1:
            if vehicle == "tractor":
                print("C")
            elif vehicle == "minivan":
                print("B")
            elif vehicle == "truck":
                print("A")
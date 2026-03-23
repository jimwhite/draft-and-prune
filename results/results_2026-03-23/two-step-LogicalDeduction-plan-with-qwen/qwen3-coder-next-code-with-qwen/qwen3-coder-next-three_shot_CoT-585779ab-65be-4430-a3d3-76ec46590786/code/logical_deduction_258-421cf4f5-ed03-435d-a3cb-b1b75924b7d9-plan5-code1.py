from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "truck", "minivan"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is newer than the truck" -> minivan > truck
problem.addConstraint(lambda minivan, truck: minivan > truck, ("minivan", "truck"))

# "The tractor is older than the truck" -> tractor < truck
problem.addConstraint(lambda tractor, truck: tractor < truck, ("tractor", "truck"))

# Solve the problem
solutions = problem.getSolutions()

# Determine which vehicle is second-newest (rank 2)
for solution in solutions:
    if solution["tractor"] == 2:
        print("A")
    elif solution["truck"] == 2:
        print("B")
    elif solution["minivan"] == 2:
        print("C")
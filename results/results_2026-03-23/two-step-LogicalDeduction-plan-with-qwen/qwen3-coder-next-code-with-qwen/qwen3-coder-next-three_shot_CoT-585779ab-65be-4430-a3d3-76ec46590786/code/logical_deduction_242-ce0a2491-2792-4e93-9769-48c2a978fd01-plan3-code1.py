from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "bus", "sedan"]
ranks = range(1, 4)  # 1=oldest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The minivan is newer than the sedan" -> minivan > sedan
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# "The minivan is older than the bus" -> minivan < bus
problem.addConstraint(lambda minivan, bus: minivan < bus, ("minivan", "bus"))

# Solve the problem
solutions = problem.getSolutions()

# Determine which vehicle is oldest (rank 1)
for solution in solutions:
    if solution["minivan"] == 1:
        print("A")
    elif solution["bus"] == 1:
        print("B")
    elif solution["sedan"] == 1:
        print("C")
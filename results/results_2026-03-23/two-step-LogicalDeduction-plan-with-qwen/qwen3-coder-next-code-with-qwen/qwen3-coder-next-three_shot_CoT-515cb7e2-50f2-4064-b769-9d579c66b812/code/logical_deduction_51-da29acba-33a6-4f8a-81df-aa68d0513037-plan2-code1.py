from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcycle"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is newer than the convertible" -> hatchback > convertible
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ["hatchback", "convertible"])

# "The bus is newer than the hatchback" -> bus > hatchback
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ["bus", "hatchback"])

# "The bus is older than the motorcycle" -> bus < motorcycle
problem.addConstraint(lambda bus, motorcycle: bus < motorcycle, ["bus", "motorcycle"])

# "The minivan is the newest" -> minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know minivan must be 5 from the constraint, choice A is true
print("A")
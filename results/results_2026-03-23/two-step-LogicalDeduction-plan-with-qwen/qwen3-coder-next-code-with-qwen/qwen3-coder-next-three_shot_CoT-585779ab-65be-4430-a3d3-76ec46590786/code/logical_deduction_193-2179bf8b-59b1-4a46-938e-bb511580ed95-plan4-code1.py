from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["limousine", "sedan", "tractor", "motorcyle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The minivan is newer than the limousine" → minivan > limousine
problem.addConstraint(lambda minivan, limousine: minivan > limousine, ("minivan", "limousine"))

# 2. "The tractor is the second-newest" → tractor == 6
problem.addConstraint(lambda tractor: tractor == 6, ("tractor",))

# 3. "The truck is older than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# 4. "The minivan is older than the truck" → minivan < truck
problem.addConstraint(lambda minivan, truck: minivan < truck, ("minivan", "truck"))

# 5. "The hatchback is newer than the tractor" → hatchback > tractor
problem.addConstraint(lambda hatchback, tractor: hatchback > tractor, ("hatchback", "tractor"))

# 6. "The motorcyle is the fourth-newest" → position 4 (newest=7, 2nd-newest=6, 3rd-newest=5, 4th-newest=4)
problem.addConstraint(lambda motorcyle: motorcyle == 4, ("motorcyle",))

# Solve the problem
solutions = problem.getSolutions()

# Since we know from constraints that tractor == 6 (second-newest), and the problem is consistent,
# we can directly check which vehicle has rank 6 in the solution
for solution in solutions:
    # The question asks which vehicle is second-newest (rank 6)
    if solution["tractor"] == 6:
        print("C")
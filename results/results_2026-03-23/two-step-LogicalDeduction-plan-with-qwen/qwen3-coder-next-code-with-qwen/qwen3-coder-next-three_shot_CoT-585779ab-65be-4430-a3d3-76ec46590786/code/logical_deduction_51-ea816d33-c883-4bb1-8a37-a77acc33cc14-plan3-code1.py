from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcyle"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is newer than the convertible" → hatchback > convertible
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ("hatchback", "convertible"))

# "The bus is newer than the hatchback" → bus > hatchback
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ("bus", "hatchback"))

# "The bus is older than the motorcyle" → bus < motorcyle
problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ("bus", "motorcyle"))

# "The minivan is the newest" → minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

# Solve the problem
solutions = problem.getSolutions()

# Check which vehicle is at position 5 (newest)
for solution in solutions:
    if solution["minivan"] == 5:
        print("A")
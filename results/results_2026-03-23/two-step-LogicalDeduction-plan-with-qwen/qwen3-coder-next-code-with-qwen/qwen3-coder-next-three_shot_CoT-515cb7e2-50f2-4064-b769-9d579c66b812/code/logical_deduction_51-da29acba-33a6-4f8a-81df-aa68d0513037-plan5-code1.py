from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcycle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have distinct age ranks
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is newer than the convertible" → hatchback > convertible
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ("hatchback", "convertible"))

# "The bus is newer than the hatchback" → bus > hatchback
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ("bus", "hatchback"))

# "The bus is older than the motorcycle" → bus < motorcycle
problem.addConstraint(lambda bus, motorcycle: bus < motorcycle, ("bus", "motorcycle"))

# "The minivan is the newest" → minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

# Solve the problem
solutions = problem.getSolutions()

# Since we know minivan must be 5 from the constraint, choice A is necessarily true
# But to follow the plan and verify with the solution:
for solution in solutions:
    # Check if minivan is indeed 5 (should always be true due to constraint)
    if solution["minivan"] == 5:
        print("A")
        break
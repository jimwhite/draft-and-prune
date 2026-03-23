from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (corrected spelling of motorcycle)
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcycle"]

# Define domain: 1 = oldest, 5 = newest
positions = range(1, 6)
problem.addVariables(vehicles, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hatchback is newer than the convertible" → hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# "The bus is newer than the hatchback" → bus < hatchback
problem.addConstraint(lambda bus, hatchback: bus < hatchback, ["bus", "hatchback"])

# "The bus is older than the motorcycle" → motorcycle < bus
problem.addConstraint(lambda motorcycle, bus: motorcycle < bus, ["motorcycle", "bus"])

# "The minivan is the newest" → minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Since we have a unique solution, take the first one
solution = solutions[0]

# Check which choice is true - the question asks for a true statement
# Choice A states "The minivan is the newest", which we've constrained to be true
# Verify that minivan == 5 in our solution (it must be by constraint)
if solution["minivan"] == 5:
    print("A")
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcycle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is newer than the convertible" → hatchback > convertible
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ["hatchback", "convertible"])

# "The bus is newer than the hatchback" → bus > hatchback
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ["bus", "hatchback"])

# "The bus is older than the motorcycle" → bus < motorcycle
problem.addConstraint(lambda bus, motorcycle: bus < motorcycle, ["bus", "motorcycle"])

# "The minivan is the newest" → minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "minivan",
    "B": "hatchback",
    "C": "bus",
    "D": "convertible",
    "E": "motorcycle"
}

# Find which vehicle has rank 5 (newest)
for solution in solutions:
    for letter, vehicle in choices.items():
        if solution[vehicle] == 5:
            print(letter)
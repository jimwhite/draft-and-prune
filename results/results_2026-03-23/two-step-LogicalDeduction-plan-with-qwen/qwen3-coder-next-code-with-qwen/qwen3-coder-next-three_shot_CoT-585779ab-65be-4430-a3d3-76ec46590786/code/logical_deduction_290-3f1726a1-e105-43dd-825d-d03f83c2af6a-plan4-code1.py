from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "convertible", "minivan"]
ranks = range(1, 4)  # 1=newest, 3=oldest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is the second-newest" -> rank 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# "The minivan is newer than the convertible" -> minivan rank < convertible rank
problem.addConstraint(lambda minivan, convertible: minivan < convertible, ["minivan", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "tractor",
    "B": "convertible",
    "C": "minivan"
}

# Find which vehicle has rank 1 (newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
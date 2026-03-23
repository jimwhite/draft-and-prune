from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "tractor", "hatchback"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is older than the convertible"
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# "The tractor is the newest"
problem.addConstraint(lambda tractor: tractor == 3, ["tractor"])

# Solve
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "convertible",
    "B": "tractor",
    "C": "hatchback"
}

# Find which vehicle has rank 2 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "truck", "minivan"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The minivan is newer than the truck" → minivan > truck
problem.addConstraint(lambda minivan, truck: minivan > truck, ("minivan", "truck"))

# "The tractor is older than the truck" → tractor < truck
problem.addConstraint(lambda tractor, truck: tractor < truck, ("tractor", "truck"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "tractor",
    "B": "truck",
    "C": "minivan"
}

# Find which vehicle is the oldest (rank 1) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
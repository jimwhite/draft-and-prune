from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "truck", "minivan"]
ranks = range(1, 4)  # 1=oldest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is newer than the truck" => minivan > truck
problem.addConstraint(lambda truck, minivan: minivan > truck, ("truck", "minivan"))

# "The tractor is older than the truck" => tractor < truck
problem.addConstraint(lambda tractor, truck: tractor < truck, ("tractor", "truck"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "tractor",
    "B": "truck",
    "C": "minivan"
}

# Find which vehicle is the oldest (rank 1)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
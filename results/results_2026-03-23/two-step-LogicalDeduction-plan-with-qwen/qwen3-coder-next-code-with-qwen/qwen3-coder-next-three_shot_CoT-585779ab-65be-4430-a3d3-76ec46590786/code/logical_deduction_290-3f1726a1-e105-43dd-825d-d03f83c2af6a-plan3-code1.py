from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "convertible", "minivan"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is the second-newest" -> rank 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# "The minivan is newer than the convertible" -> minivan > convertible
problem.addConstraint(lambda minivan, convertible: minivan > convertible, ["minivan", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to conditions (which vehicle is newest, i.e., rank 3)
choices = {
    "A": "tractor",
    "B": "convertible", 
    "C": "minivan"
}

# Find which vehicle has rank 3 (newest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle in choices.items():
        if solution[vehicle] == 3:
            print(letter)
from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["truck", "minivan", "tractor"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The truck is newer than the minivan" -> truck's rank > minivan's rank
problem.addConstraint(lambda truck, minivan: truck > minivan, ("truck", "minivan"))

# "The minivan is newer than the tractor" -> minivan's rank > tractor's rank
problem.addConstraint(lambda minivan, tractor: minivan > tractor, ("minivan", "tractor"))

# Solve for the arrangement
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "minivan",
    "C": "tractor"
}

# Find the vehicle with rank 1 (oldest) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
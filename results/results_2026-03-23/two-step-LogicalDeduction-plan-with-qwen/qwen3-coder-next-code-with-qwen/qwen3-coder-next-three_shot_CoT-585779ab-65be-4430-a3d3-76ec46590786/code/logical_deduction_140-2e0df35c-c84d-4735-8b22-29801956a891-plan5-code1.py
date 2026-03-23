from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["limousine", "sedan", "tractor", "motorcyle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)  # 1=oldest, 7=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The minivan is newer than the limousine" → minivan > limousine
problem.addConstraint(lambda minivan, limousine: minivan > limousine, ("minivan", "limousine"))

# "The tractor is the second-newest" → tractor == 6
problem.addConstraint(lambda tractor: tractor == 6, ("tractor",))

# "The truck is older than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# "The minivan is older than the truck" → minivan < truck
problem.addConstraint(lambda minivan, truck: minivan < truck, ("minivan", "truck"))

# "The hatchback is newer than the tractor" → hatchback > tractor
problem.addConstraint(lambda hatchback, tractor: hatchback > tractor, ("hatchback", "tractor"))

# "The motorcyle is the fourth-newest" → motorcyle == 4
problem.addConstraint(lambda motorcyle: motorcyle == 4, ("motorcyle",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "limousine",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcyle",
    "E": "minivan",
    "F": "hatchback",
    "G": "truck"
}

# Find which vehicle has rank 7 (newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 7:
            print(letter)
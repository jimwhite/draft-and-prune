from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["sedan", "minivan", "motorcycle", "limousine", "hatchback", "truck", "tractor"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The motorcycle is older than the tractor" → motorcycle < tractor
problem.addConstraint(lambda motorcycle, tractor: motorcycle < tractor, ("motorcycle", "tractor"))

# "The hatchback is older than the limousine" → hatchback < limousine
problem.addConstraint(lambda hatchback, limousine: hatchback < limousine, ("hatchback", "limousine"))

# "The hatchback is newer than the truck" → truck < hatchback
problem.addConstraint(lambda truck, hatchback: truck < hatchback, ("truck", "hatchback"))

# "The truck is newer than the tractor" → tractor < truck
problem.addConstraint(lambda tractor, truck: tractor < truck, ("tractor", "truck"))

# "The minivan is the second-newest" → minivan == 6
problem.addConstraint(lambda minivan: minivan == 6, ("minivan",))

# "The sedan is the third-newest" → sedan == 5
problem.addConstraint(lambda sedan: sedan == 5, ("sedan",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "sedan",
    "B": "minivan",
    "C": "motorcycle",
    "D": "limousine",
    "E": "hatchback",
    "F": "truck",
    "G": "tractor"
}

# Find which vehicle has rank 4 (fourth-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
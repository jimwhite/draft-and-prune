from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["limousine", "sedan", "tractor", "motorcycle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The minivan is newer than the limousine" → minivan > limousine
problem.addConstraint(lambda limousine, minivan: minivan > limousine, ("limousine", "minivan"))

# "The tractor is the second-newest" → tractor == 6
problem.addConstraint(lambda tractor: tractor == 6, ("tractor",))

# "The truck is older than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# "The minivan is older than the truck" → minivan < truck
problem.addConstraint(lambda minivan, truck: minivan < truck, ("minivan", "truck"))

# "The hatchback is newer than the tractor" → hatchback > tractor
problem.addConstraint(lambda hatchback, tractor: hatchback > tractor, ("hatchback", "tractor"))

# "The motorcycle is the fourth-newest" → motorcycle == 4
problem.addConstraint(lambda motorcycle: motorcycle == 4, ("motorcycle",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "limousine",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcycle",
    "E": "minivan",
    "F": "hatchback",
    "G": "truck"
}

# Find which vehicle is the newest (rank 7)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 7:
            print(letter)
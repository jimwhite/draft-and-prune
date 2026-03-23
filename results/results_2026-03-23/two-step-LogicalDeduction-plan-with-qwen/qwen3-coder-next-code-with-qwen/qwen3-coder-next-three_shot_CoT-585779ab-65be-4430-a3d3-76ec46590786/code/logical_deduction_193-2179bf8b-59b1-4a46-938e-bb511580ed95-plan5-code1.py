from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["limousine", "sedan", "tractor", "motorcycle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferentConstraint to ensure unique positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. "The minivan is newer than the limousine" → minivan > limousine
problem.addConstraint(lambda limousine, minivan: minivan > limousine, ("limousine", "minivan"))

# 2. "The tractor is the second-newest" → tractor == 6
problem.addConstraint(lambda tractor: tractor == 6, ("tractor",))

# 3. "The truck is older than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# 4. "The minivan is older than the truck" → minivan < truck
problem.addConstraint(lambda minivan, truck: minivan < truck, ("minivan", "truck"))

# 5. "The hatchback is newer than the tractor" → hatchback > tractor
# Since tractor == 6, this means hatchback > 6, so hatchback == 7
problem.addConstraint(lambda hatchback: hatchback > 6, ("hatchback",))

# 6. "The motorcyle is the fourth-newest" → fourth-newest = position 4 (since 7=newest, 6=2nd-newest, etc.)
problem.addConstraint(lambda motorcycle: motorcycle == 4, ("motorcycle",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for the second-newest position (rank 6)
choices = {
    "A": "limousine",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcycle",
    "E": "minivan",
    "F": "hatchback",
    "G": "truck"
}

# Find which vehicle has rank 6 (second-newest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 6:
            print(letter)
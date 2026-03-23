from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=newest, 7=oldest)
vehicles = ["limousine", "sedan", "tractor", "motorcyle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The minivan is newer than the limousine" → minivan < limousine
problem.addConstraint(lambda minivan, limousine: minivan < limousine, ("minivan", "limousine"))

# 2. "The tractor is the second-newest" → tractor == 2
problem.addConstraint(lambda tractor: tractor == 2, ("tractor",))

# 3. "The truck is older than the sedan" → truck > sedan
problem.addConstraint(lambda truck, sedan: truck > sedan, ("truck", "sedan"))

# 4. "The minivan is older than the truck" → minivan > truck
problem.addConstraint(lambda minivan, truck: minivan > truck, ("minivan", "truck"))

# 5. "The hatchback is newer than the tractor" → hatchback < tractor (i.e., hatchback < 2)
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ("hatchback", "tractor"))

# 6. "The motorcyle is the fourth-newest" → motorcyle == 4
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

# Find which vehicle is the newest (rank 1) and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
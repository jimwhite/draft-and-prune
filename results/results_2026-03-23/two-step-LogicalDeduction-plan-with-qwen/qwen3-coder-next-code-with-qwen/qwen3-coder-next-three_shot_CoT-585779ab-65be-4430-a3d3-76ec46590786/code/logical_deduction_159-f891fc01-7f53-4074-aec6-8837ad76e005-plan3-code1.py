from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["limousine", "sedan", "tractor", "motorcyle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is newer than the limousine" → minivan > limousine
problem.addConstraint(lambda limousine, minivan: minivan > limousine, ("limousine", "minivan"))

# 3. "The tractor is the second-newest" → tractor == 6
problem.addConstraint(lambda tractor: tractor == 6, ("tractor",))

# 4. "The truck is older than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# 5. "The minivan is older than the truck" → minivan < truck
problem.addConstraint(lambda minivan, truck: minivan < truck, ("minivan", "truck"))

# 6. "The hatchback is newer than the tractor" → hatchback > tractor
problem.addConstraint(lambda hatchback, tractor: hatchback > tractor, ("hatchback", "tractor"))

# 7. "The motorcyle is the fourth-newest" → motorcyle == 4 (since 7-3=4)
problem.addConstraint(lambda motorcyle: motorcyle == 4, ("motorcyle",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': 'limousine',
    'B': 'sedan',
    'C': 'tractor',
    'D': 'motorcyle',
    'E': 'minivan',
    'F': 'hatchback',
    'G': 'truck'
}

# Find which vehicle is at position 3 (third-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
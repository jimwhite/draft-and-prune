from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["sedan", "minivan", "motorcyle", "limousine", "hatchback", "truck", "tractor"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The motorcyle is older than the tractor" → motorcyle < tractor
problem.addConstraint(lambda motorcyle, tractor: motorcyle < tractor, ("motorcyle", "tractor"))

# 3. "The hatchback is older than the limousine" → hatchback < limousine
problem.addConstraint(lambda hatchback, limousine: hatchback < limousine, ("hatchback", "limousine"))

# 4. "The hatchback is newer than the truck" → truck < hatchback
problem.addConstraint(lambda truck, hatchback: truck < hatchback, ("truck", "hatchback"))

# 5. "The truck is newer than the tractor" → tractor < truck
problem.addConstraint(lambda tractor, truck: tractor < truck, ("tractor", "truck"))

# 6. "The minivan is the second-newest" → minivan == 6
problem.addConstraint(lambda minivan: minivan == 6, ("minivan",))

# 7. "The sedan is the third-newest" → sedan == 5
problem.addConstraint(lambda sedan: sedan == 5, ("sedan",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': 'sedan',
    'B': 'minivan',
    'C': 'motorcyle',
    'D': 'limousine',
    'E': 'hatchback',
    'F': 'truck',
    'G': 'tractor'
}

# Find which vehicle has rank 4 (fourth-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
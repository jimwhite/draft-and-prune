from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["limousine", "truck", "sedan", "tractor", "minivan", "motorcyle", "hatchback"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The minivan is older than the tractor" → minivan < tractor
problem.addConstraint(lambda minivan, tractor: minivan < tractor, ("minivan", "tractor"))

# 2. "The hatchback is older than the sedan" → hatchback < sedan
problem.addConstraint(lambda hatchback, sedan: hatchback < sedan, ("hatchback", "sedan"))

# 3. "The truck is the third-newest" → truck == 5
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# 4. "The hatchback is the second-newest" → hatchback == 6
problem.addConstraint(lambda hatchback: hatchback == 6, ("hatchback",))

# 5. "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# 6. "The motorcyle is newer than the limousine" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ("limousine", "motorcyle"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': 'limousine',
    'B': 'truck',
    'C': 'sedan',
    'D': 'tractor',
    'E': 'minivan',
    'F': 'motorcyle',
    'G': 'hatchback'
}

# Find which vehicle has rank 7 (newest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 7:
            print(letter)
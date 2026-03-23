from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicle variables and their domain (1=newest, 7=oldest)
vehicles = ["limousine", "sedan", "tractor", "motorcyle", "minivan", "hatchback", "truck"]
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem description
# 1. All vehicles must have different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is newer than the limousine" → minivan < limousine
problem.addConstraint(lambda minivan, limousine: minivan < limousine, ("minivan", "limousine"))

# 3. "The tractor is the second-newest" → tractor == 2
problem.addConstraint(lambda tractor: tractor == 2, ("tractor",))

# 4. "The truck is older than the sedan" → truck > sedan
problem.addConstraint(lambda truck, sedan: truck > sedan, ("truck", "sedan"))

# 5. "The minivan is older than the truck" → minivan > truck
problem.addConstraint(lambda minivan, truck: minivan > truck, ("minivan", "truck"))

# 6. "The hatchback is newer than the tractor" → hatchback < tractor
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ("hatchback", "tractor"))

# 7. "The motorcyle is the fourth-newest" → motorcyle == 4
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

# Find the vehicle with position 1 (newest) and print its corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
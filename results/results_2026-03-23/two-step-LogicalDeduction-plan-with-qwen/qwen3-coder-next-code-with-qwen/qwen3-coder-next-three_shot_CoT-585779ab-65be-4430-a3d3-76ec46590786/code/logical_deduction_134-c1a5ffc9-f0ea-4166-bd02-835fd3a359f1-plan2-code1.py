from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["limousine", "truck", "sedan", "tractor", "minivan", "motorcycle", "hatchback"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The minivan is older than the tractor" → minivan < tractor
problem.addConstraint(lambda minivan, tractor: minivan < tractor, ("minivan", "tractor"))

# "The hatchback is older than the sedan" → hatchback < sedan
problem.addConstraint(lambda hatchback, sedan: hatchback < sedan, ("hatchback", "sedan"))

# "The truck is the third-newest" → truck == 5 (since 7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# "The hatchback is the second-newest" → hatchback == 6
problem.addConstraint(lambda hatchback: hatchback == 6, ("hatchback",))

# "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The motorcyle is newer than the limousine" → limousine < motorcycle
problem.addConstraint(lambda limousine, motorcycle: limousine < motorcycle, ("limousine", "motorcycle"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': "limousine",
    'B': "truck",
    'C': "sedan",
    'D': "tractor",
    'E': "minivan",
    'F': "motorcycle",
    'G': "hatchback"
}

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
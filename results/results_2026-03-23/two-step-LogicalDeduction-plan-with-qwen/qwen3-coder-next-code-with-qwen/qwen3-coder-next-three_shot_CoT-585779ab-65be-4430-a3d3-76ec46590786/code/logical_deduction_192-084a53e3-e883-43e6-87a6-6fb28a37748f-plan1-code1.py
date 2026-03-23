from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["limousine", "truck", "sedan", "tractor", "minivan", "motorcyle", "hatchback"]
positions = range(1, 8)  # 1=oldest, 7=newest
problem.addVariables(vehicles, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the tractor" → minivan < tractor
problem.addConstraint(lambda minivan, tractor: minivan < tractor, ("minivan", "tractor"))

# "The hatchback is older than the sedan" → hatchback < sedan
problem.addConstraint(lambda hatchback, sedan: hatchback < sedan, ("hatchback", "sedan"))

# "The truck is the third-newest" → truck == 5 (since newest=7, second-newest=6, third-newest=5)
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# "The hatchback is the second-newest" → hatchback == 6
problem.addConstraint(lambda hatchback: hatchback == 6, ("hatchback",))

# "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The motorcyle is newer than the limousine" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ("limousine", "motorcyle"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "limousine",
    "B": "truck",
    "C": "sedan",
    "D": "tractor",
    "E": "minivan",
    "F": "motorcyle",
    "G": "hatchback"
}

# Find which vehicle is at position 4 (fourth-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
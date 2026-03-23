from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "limousine", "sedan", "tractor", "hatchback"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is the second-newest" -> position 4
problem.addConstraint(lambda tractor: tractor == 4, ["tractor"])

# "The limousine is newer than the hatchback" -> limousine > hatchback
problem.addConstraint(lambda limousine, hatchback: limousine > hatchback, ["limousine", "hatchback"])

# "The limousine is older than the sedan" -> limousine < sedan
problem.addConstraint(lambda limousine, sedan: limousine < sedan, ["limousine", "sedan"])

# "The minivan is newer than the sedan" -> minivan > sedan
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ["minivan", "sedan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "minivan",
    "B": "limousine",
    "C": "sedan",
    "D": "tractor",
    "E": "hatchback"
}

# Find the vehicle with rank 1 (oldest) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
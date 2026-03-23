from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "limousine", "sedan", "tractor", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is the second-newest" -> rank 4
problem.addConstraint(lambda tractor: tractor == 4, ["tractor"])

# "The limousine is newer than the hatchback" -> hatchback < limousine
problem.addConstraint(lambda hatchback, limousine: hatchback < limousine, ["hatchback", "limousine"])

# "The limousine is older than the sedan" -> limousine < sedan
problem.addConstraint(lambda limousine, sedan: limousine < sedan, ["limousine", "sedan"])

# "The minivan is newer than the sedan" -> sedan < minivan
problem.addConstraint(lambda sedan, minivan: sedan < minivan, ["sedan", "minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "minivan",
    "B": "limousine",
    "C": "sedan",
    "D": "tractor",
    "E": "hatchback"
}

# Find which vehicle is the oldest (rank 1)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
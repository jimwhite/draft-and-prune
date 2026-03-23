from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["minivan", "limousine", "sedan", "tractor", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is the second-newest" → rank 4
problem.addConstraint(lambda tractor: tractor == 4, ["tractor"])

# 3. "The limousine is newer than the hatchback" → hatchback < limousine
problem.addConstraint(lambda hatchback, limousine: hatchback < limousine, ["hatchback", "limousine"])

# 4. "The limousine is older than the sedan" → limousine < sedan
problem.addConstraint(lambda limousine, sedan: limousine < sedan, ["limousine", "sedan"])

# 5. "The minivan is newer than the sedan" → sedan < minivan
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

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
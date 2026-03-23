from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["minivan", "limousine", "sedan", "tractor", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is the second-newest" → rank 4
problem.addConstraint(lambda tractor: tractor == 4, ["tractor"])

# 3. "The limousine is newer than the hatchback" → limousine > hatchback
problem.addConstraint(lambda limousine, hatchback: limousine > hatchback, ["limousine", "hatchback"])

# 4. "The limousine is older than the sedan" → limousine < sedan
problem.addConstraint(lambda limousine, sedan: limousine < sedan, ["limousine", "sedan"])

# 5. "The minivan is newer than the sedan" → minivan > sedan
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ["minivan", "sedan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for the question about the oldest vehicle (rank 1)
choices = {
    "A": "minivan",
    "B": "limousine",
    "C": "sedan",
    "D": "tractor",
    "E": "hatchback"
}

# Find which vehicle has rank 1 (oldest) and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
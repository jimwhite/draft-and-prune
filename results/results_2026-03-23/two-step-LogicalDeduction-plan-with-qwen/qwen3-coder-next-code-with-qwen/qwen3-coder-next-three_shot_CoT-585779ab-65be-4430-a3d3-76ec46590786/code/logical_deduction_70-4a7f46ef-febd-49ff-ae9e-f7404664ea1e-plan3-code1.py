from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["hatchback", "limousine", "sedan", "bus", "tractor"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is newer than the hatchback" → tractor > hatchback
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ["hatchback", "tractor"])

# 3. "The bus is the second-oldest" → bus == 2
problem.addConstraint(lambda bus: bus == 2, ["bus"])

# 4. "The hatchback is newer than the sedan" → hatchback > sedan
problem.addConstraint(lambda sedan, hatchback: sedan < hatchback, ["sedan", "hatchback"])

# 5. "The limousine is the newest" → limousine == 5
problem.addConstraint(lambda limousine: limousine == 5, ["limousine"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "hatchback",
    "B": "limousine",
    "C": "sedan",
    "D": "bus",
    "E": "tractor"
}

# Find the vehicle with rank 1 (oldest) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
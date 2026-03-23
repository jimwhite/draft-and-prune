from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "tractor", "hatchback"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is older than the convertible" -> hatchback rank < convertible rank
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# "The tractor is the newest" -> tractor rank == 3
problem.addConstraint(lambda tractor: tractor == 3, ["tractor"])

# Solve the problem
solutions = problem.getSolutions()
solution = solutions[0]

# Map choices to vehicles and find which has rank 2 (second-newest)
choices = {
    "A": "convertible",
    "B": "tractor",
    "C": "hatchback"
}

# Find the vehicle with rank 2 and print its corresponding choice letter
for letter, vehicle_name in choices.items():
    if solution[vehicle_name] == 2:
        print(letter)
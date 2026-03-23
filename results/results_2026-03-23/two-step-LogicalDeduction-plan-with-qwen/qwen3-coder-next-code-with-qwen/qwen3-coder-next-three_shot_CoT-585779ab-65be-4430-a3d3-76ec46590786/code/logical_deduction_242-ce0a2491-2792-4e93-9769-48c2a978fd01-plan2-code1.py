from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "bus", "sedan"]
ranks = range(1, 4)  # 1=oldest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The minivan is newer than the sedan" -> minivan > sedan
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# "The minivan is older than the bus" -> minivan < bus
problem.addConstraint(lambda minivan, bus: minivan < bus, ("minivan", "bus"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "minivan",
    "B": "bus",
    "C": "sedan"
}

# Find the vehicle with rank 1 (oldest) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
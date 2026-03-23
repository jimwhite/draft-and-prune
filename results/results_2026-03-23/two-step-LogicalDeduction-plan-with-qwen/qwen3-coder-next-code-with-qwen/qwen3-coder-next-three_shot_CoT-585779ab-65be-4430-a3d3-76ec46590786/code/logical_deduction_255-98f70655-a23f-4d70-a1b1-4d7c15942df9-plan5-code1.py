from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)  # 1=oldest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is older than the hatchback" -> station_wagon < hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# "The hatchback is the second-newest" -> rank 2 (since newest=3, second-newest=2)
problem.addConstraint(lambda hatchback: hatchback == 2, ("hatchback",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "hatchback",
    "B": "limousine",
    "C": "station_wagon"
}

# Find which vehicle has rank 1 (oldest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "limousine"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the limousine" means tractor has a higher rank number
problem.addConstraint(lambda tractor, limousine: tractor > limousine, ["tractor", "limousine"])

# "The station wagon is the newest" means rank 3
problem.addConstraint(lambda station_wagon: station_wagon == 3, ["station_wagon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "tractor",
    "B": "station_wagon",
    "C": "limousine"
}

# Find which vehicle has rank 2 (second-newest)
for solution in solutions:
    for letter, vehicle in choices.items():
        if solution[vehicle] == 2:
            print(letter)
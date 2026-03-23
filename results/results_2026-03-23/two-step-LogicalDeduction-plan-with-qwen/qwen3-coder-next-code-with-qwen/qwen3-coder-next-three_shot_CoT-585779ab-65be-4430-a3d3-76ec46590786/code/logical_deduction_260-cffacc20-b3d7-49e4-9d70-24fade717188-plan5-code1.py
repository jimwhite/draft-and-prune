from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "limousine"]
ranks = range(1, 4)  # 1=newest, 2=second-newest, 3=oldest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is the newest."
problem.addConstraint(lambda station_wagon: station_wagon == 1, ["station_wagon"])

# "The tractor is newer than the limousine."
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ["tractor", "limousine"])

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
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
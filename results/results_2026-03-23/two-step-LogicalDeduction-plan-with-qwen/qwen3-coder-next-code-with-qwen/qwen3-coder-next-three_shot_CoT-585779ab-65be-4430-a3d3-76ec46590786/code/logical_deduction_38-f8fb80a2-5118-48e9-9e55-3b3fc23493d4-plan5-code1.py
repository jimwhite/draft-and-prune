from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["sedan", "convertible", "station_wagon", "bus", "motorcycle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The sedan is the second-newest" → rank 4 (since 5=newest, 4=second-newest)
problem.addConstraint(lambda sedan: sedan == 4, ["sedan"])

# "The station wagon is newer than the convertible" → station_wagon > convertible
problem.addConstraint(lambda station_wagon, convertible: station_wagon > convertible, ["station_wagon", "convertible"])

# "The sedan is older than the motorcycle" → sedan < motorcycle
problem.addConstraint(lambda sedan, motorcycle: sedan < motorcycle, ["sedan", "motorcycle"])

# "The bus is the oldest" → rank 1
problem.addConstraint(lambda bus: bus == 1, ["bus"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "sedan",
    "B": "convertible",
    "C": "station_wagon",
    "D": "bus",
    "E": "motorcycle"
}

# Find which vehicle is second-oldest (rank 2)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 5, where 1=oldest, 5=newest)
vehicles = ["sedan", "convertible", "station_wagon", "bus", "motorcycle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The sedan is the second-newest" → rank 4
problem.addConstraint(lambda sedan: sedan == 4, ["sedan"])

# "The station wagon is newer than the convertible" → station_wagon > convertible
problem.addConstraint(lambda station_wagon, convertible: station_wagon > convertible, ["station_wagon", "convertible"])

# "The sedan is older than the motorcycle" → sedan < motorcycle
problem.addConstraint(lambda sedan, motorcycle: sedan < motorcycle, ["sedan", "motorcycle"])

# "The bus is the oldest" → rank 1
problem.addConstraint(lambda bus: bus == 1, ["bus"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "sedan",
    "B": "convertible",
    "C": "station_wagon",
    "D": "bus",
    "E": "motorcycle"
}

# Find which vehicle is at position 2 (second-oldest)
for solution in solutions:
    for letter, vehicle in choices.items():
        if solution[vehicle] == 2:
            print(letter)
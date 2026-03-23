from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["sedan", "truck", "bus", "station_wagon", "tractor", "convertible", "limousine"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The truck is the oldest"
problem.addConstraint(lambda truck: truck == 1, ["truck"])

# "The tractor is the newest"
problem.addConstraint(lambda tractor: tractor == 7, ["tractor"])

# "The sedan is older than the station wagon"
problem.addConstraint(lambda sedan, station_wagon: sedan < station_wagon, ["sedan", "station_wagon"])

# "The station wagon is the third-newest" (positions: 7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda station_wagon: station_wagon == 5, ["station_wagon"])

# "The bus is older than the convertible"
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# "The sedan is newer than the convertible"
problem.addConstraint(lambda convertible, sedan: convertible < sedan, ["convertible", "sedan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "sedan",
    "B": "truck",
    "C": "bus",
    "D": "station_wagon",
    "E": "tractor",
    "F": "convertible",
    "G": "limousine"
}

# Find the vehicle that is third-oldest (rank 3)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
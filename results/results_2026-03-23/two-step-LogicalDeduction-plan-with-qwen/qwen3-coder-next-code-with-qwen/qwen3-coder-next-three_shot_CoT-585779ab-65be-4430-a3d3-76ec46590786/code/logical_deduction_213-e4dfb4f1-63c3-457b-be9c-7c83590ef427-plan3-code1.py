from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "truck", "bus", "station_wagon", "tractor", "convertible", "limousine"]
ranks = range(1, 8)  # 1 to 7, where 1 is oldest and 7 is newest
problem.addVariables(vehicles, ranks)

# Add AllDifferentConstraint to ensure unique positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The truck is the oldest" -> truck == 1
problem.addConstraint(lambda truck: truck == 1, ["truck"])

# "The tractor is the newest" -> tractor == 7
problem.addConstraint(lambda tractor: tractor == 7, ["tractor"])

# "The sedan is older than the station wagon" -> sedan < station_wagon
problem.addConstraint(lambda sedan, station_wagon: sedan < station_wagon, ["sedan", "station_wagon"])

# "The station wagon is the third-newest" -> station_wagon == 5
problem.addConstraint(lambda station_wagon: station_wagon == 5, ["station_wagon"])

# "The bus is older than the convertible" -> bus < convertible
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# "The sedan is newer than the convertible" -> convertible < sedan
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

# Find the vehicle that is third-oldest (rank = 3)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
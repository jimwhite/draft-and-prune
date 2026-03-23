from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles)
vehicles = ["sedan", "truck", "bus", "station_wagon", "tractor", "convertible", "limousine"]

# Define domain: positions 1 to 7, where 1 = oldest, 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem description
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The truck is the oldest" → truck == 1
problem.addConstraint(lambda truck: truck == 1, ["truck"])

# 3. "The tractor is the newest" → tractor == 7
problem.addConstraint(lambda tractor: tractor == 7, ["tractor"])

# 4. "The sedan is older than the station wagon" → sedan < station_wagon
problem.addConstraint(lambda sedan, station_wagon: sedan < station_wagon, ["sedan", "station_wagon"])

# 5. "The station wagon is the third-newest" → position 5 (since newest=7, third-newest = 7-2 = 5)
problem.addConstraint(lambda station_wagon: station_wagon == 5, ["station_wagon"])

# 6. "The bus is older than the convertible" → bus < convertible
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# 7. "The sedan is newer than the convertible" → convertible < sedan
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

# Find which vehicle is third-oldest (rank 3)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
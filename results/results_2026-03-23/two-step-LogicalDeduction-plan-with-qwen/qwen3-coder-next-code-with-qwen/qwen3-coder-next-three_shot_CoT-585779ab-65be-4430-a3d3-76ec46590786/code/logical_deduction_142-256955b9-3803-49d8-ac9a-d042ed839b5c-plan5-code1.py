from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Absolute position constraints:
# "The station wagon is the fourth-newest" → rank 4 (7-3=4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])
# "The minivan is the third-newest" → rank 5 (7-2=5)
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])
# "The tractor is the second-oldest" → rank 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# Relative order constraints:
# "The convertible is older than the station wagon" → convertible < station_wagon
problem.addConstraint(lambda convertible, station_wagon: convertible < station_wagon, ["convertible", "station_wagon"])
# "The truck is newer than the bus" → bus < truck
problem.addConstraint(lambda bus, truck: bus < truck, ["bus", "truck"])
# "The hatchback is older than the convertible" → hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "hatchback",
    "C": "minivan",
    "D": "bus",
    "E": "tractor",
    "F": "station_wagon",
    "G": "convertible"
}

# Find the vehicle with rank 7 (newest) and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 7:
            print(letter)
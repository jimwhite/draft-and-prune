from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]

# Define the domain: positions 1 to 7, where 1 = oldest and 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraint that all vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is the fourth-newest" -> rank = 4 (since 7-4+1=4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# "The minivan is the third-newest" -> rank = 5 (since 7-3+1=5)
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# "The tractor is the second-oldest" -> rank = 2 (since oldest=1, second-oldest=2)
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# "The convertible is older than the station wagon" -> convertible rank < station_wagon rank (convertible < 4)
problem.addConstraint(lambda convertible, station_wagon: convertible < station_wagon, ["convertible", "station_wagon"])

# "The truck is newer than the bus" -> bus rank < truck rank (bus older, truck newer)
problem.addConstraint(lambda bus, truck: bus < truck, ["bus", "truck"])

# "The hatchback is older than the convertible" -> hatchback rank < convertible rank
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

# Find the vehicle with rank 7 (newest) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 7:
            print(letter)
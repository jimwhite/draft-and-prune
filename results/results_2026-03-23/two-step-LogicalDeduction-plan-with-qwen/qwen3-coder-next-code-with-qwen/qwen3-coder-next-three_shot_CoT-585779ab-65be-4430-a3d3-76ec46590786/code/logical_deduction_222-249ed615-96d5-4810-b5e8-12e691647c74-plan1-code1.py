from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]

# Define the domain: positions 1 to 7, where 1 is oldest and 7 is newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraint that all vehicles have different positions
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is the fourth-newest" -> position = 4 (since 7-3=4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# "The minivan is the third-newest" -> position = 5 (since 7-2=5)
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# "The tractor is the second-oldest" -> position = 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# "The convertible is older than the station wagon" -> convertible < station_wagon (i.e., convertible < 4)
problem.addConstraint(lambda convertible, station_wagon: convertible < station_wagon, ["convertible", "station_wagon"])

# "The truck is newer than the bus" -> truck > bus (i.e., bus < truck)
problem.addConstraint(lambda bus, truck: bus < truck, ["bus", "truck"])

# "The hatchback is older than the convertible" -> hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Get the solution(s)
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

# Find the vehicle with rank 1 (oldest) and print its corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
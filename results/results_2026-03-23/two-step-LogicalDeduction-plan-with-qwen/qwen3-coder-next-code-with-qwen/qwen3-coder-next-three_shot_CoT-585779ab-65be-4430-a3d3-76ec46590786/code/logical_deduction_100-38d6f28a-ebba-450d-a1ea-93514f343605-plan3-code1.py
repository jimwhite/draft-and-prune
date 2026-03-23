from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferentConstraint to ensure each vehicle has a unique rank
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# "The station wagon is the fourth-newest" → rank 4 (since newest=7, fourth-newest=4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# "The minivan is the third-newest" → rank 5
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# "The tractor is the second-oldest" → rank 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# "The convertible is older than the station wagon" → convertible < station_wagon
problem.addConstraint(lambda convertible, station_wagon: convertible < station_wagon, ["convertible", "station_wagon"])

# "The truck is newer than the bus" → bus < truck
problem.addConstraint(lambda bus, truck: bus < truck, ["bus", "truck"])

# "The hatchback is older than the convertible" → hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks for the vehicle that is second-newest (rank 6)
choices = {
    'A': "truck",
    'B': "hatchback",
    'C': "minivan",
    'D': "bus",
    'E': "tractor",
    'F': "station_wagon",
    'G': "convertible"
}

# Find the vehicle with rank 6 and print its corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 6:
            print(letter)
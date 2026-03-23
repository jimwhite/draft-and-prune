from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["station_wagon", "sedan", "bus", "motorcycle", "hatchback", "tractor", "minivan"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The sedan is the third-oldest" -> rank 3
problem.addConstraint(lambda sedan: sedan == 3, ["sedan"])

# "The tractor is newer than the motorcycle" -> motorcycle < tractor
problem.addConstraint(lambda motorcycle, tractor: motorcycle < tractor, ["motorcycle", "tractor"])

# "The bus is older than the motorcycle" -> bus < motorcycle
problem.addConstraint(lambda bus, motorcycle: bus < motorcycle, ["bus", "motorcycle"])

# "The bus is newer than the hatchback" -> hatchback < bus
problem.addConstraint(lambda hatchback, bus: hatchback < bus, ["hatchback", "bus"])

# "The minivan is the newest" -> rank 7
problem.addConstraint(lambda minivan: minivan == 7, ["minivan"])

# "The station wagon is the oldest" -> rank 1
problem.addConstraint(lambda station_wagon: station_wagon == 1, ["station_wagon"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "station_wagon",
    "B": "sedan",
    "C": "bus",
    "D": "motorcycle",
    "E": "hatchback",
    "F": "tractor",
    "G": "minivan"
}

# Find the second-oldest vehicle (rank 2) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
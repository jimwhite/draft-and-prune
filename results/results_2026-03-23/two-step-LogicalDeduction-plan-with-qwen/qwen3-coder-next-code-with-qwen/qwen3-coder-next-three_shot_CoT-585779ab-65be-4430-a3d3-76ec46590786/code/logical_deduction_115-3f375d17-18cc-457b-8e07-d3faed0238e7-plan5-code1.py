from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["convertible", "limousine", "hatchback", "bus", "station_wagon", "tractor", "minivan"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is the fourth-newest" → rank 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# "The hatchback is older than the bus" → hatchback < bus
problem.addConstraint(lambda hatchback, bus: hatchback < bus, ["hatchback", "bus"])

# "The hatchback is the second-newest" → rank 6
problem.addConstraint(lambda hatchback: hatchback == 6, ["hatchback"])

# "The minivan is newer than the limousine" → limousine < minivan
problem.addConstraint(lambda limousine, minivan: limousine < minivan, ["limousine", "minivan"])

# "The convertible is older than the limousine" → convertible < limousine
problem.addConstraint(lambda convertible, limousine: convertible < limousine, ["convertible", "limousine"])

# "The tractor is the second-oldest" → rank 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': "convertible",
    'B': "limousine",
    'C': "hatchback",
    'D': "bus",
    'E': "station_wagon",
    'F': "tractor",
    'G': "minivan"
}

# Find the vehicle with rank 5 (third-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
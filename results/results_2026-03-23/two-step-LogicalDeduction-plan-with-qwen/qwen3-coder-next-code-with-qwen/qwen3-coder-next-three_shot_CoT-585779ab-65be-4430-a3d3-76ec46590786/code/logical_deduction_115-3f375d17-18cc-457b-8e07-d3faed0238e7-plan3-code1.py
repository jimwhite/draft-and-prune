from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["convertible", "limousine", "hatchback", "bus", "station_wagon", "tractor", "minivan"]

# Define the domain: positions 1 to 7, where 1 = oldest and 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem description
# 1. All vehicles must have unique age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest" → position = 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# 3. "The hatchback is older than the bus" → hatchback < bus
problem.addConstraint(lambda hatchback, bus: hatchback < bus, ["hatchback", "bus"])

# 4. "The hatchback is the second-newest" → position = 6
problem.addConstraint(lambda hatchback: hatchback == 6, ["hatchback"])

# 5. "The minivan is newer than the limousine" → limousine < minivan
problem.addConstraint(lambda limousine, minivan: limousine < minivan, ["limousine", "minivan"])

# 6. "The convertible is older than the limousine" → convertible < limousine
problem.addConstraint(lambda convertible, limousine: convertible < limousine, ["convertible", "limousine"])

# 7. "The tractor is the second-oldest" → position = 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "convertible",
    "B": "limousine",
    "C": "hatchback",
    "D": "bus",
    "E": "station_wagon",
    "F": "tractor",
    "G": "minivan"
}

# Find the vehicle that is third-newest (position = 5)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
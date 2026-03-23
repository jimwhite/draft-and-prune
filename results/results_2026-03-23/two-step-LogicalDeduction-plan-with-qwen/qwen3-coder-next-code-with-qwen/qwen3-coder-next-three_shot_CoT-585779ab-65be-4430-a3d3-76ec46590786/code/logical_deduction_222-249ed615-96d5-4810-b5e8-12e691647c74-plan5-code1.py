from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["truck", "hatchback", "minivan", "bus", "tractor", "station_wagon", "convertible"]

# Define the domain: positions 1 to 7, where 1 = oldest and 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem description
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest" → rank = 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# 3. "The minivan is the third-newest" → rank = 3
problem.addConstraint(lambda minivan: minivan == 3, ["minivan"])

# 4. "The tractor is the second-oldest" → rank = 2
problem.addConstraint(lambda tractor: tractor == 2, ["tractor"])

# 5. "The convertible is older than the station wagon" → convertible < 4
problem.addConstraint(lambda convertible: convertible < 4, ["convertible"])

# 6. "The truck is newer than the bus" → truck > bus
problem.addConstraint(lambda truck, bus: truck > bus, ["truck", "bus"])

# 7. "The hatchback is older than the convertible" → hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Find all solutions
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
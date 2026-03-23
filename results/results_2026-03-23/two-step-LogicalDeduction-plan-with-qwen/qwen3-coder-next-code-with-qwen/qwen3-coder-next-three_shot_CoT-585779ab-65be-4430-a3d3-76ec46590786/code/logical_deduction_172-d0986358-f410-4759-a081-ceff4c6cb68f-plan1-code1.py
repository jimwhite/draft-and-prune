from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["limousine", "convertible", "station_wagon", "minivan", "bus", "tractor", "truck"]

# Define the domain: positions 1 to 7, where 1 = oldest and 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem description
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is the oldest."
problem.addConstraint(lambda minivan: minivan == 1, ["minivan"])

# 3. "The truck is older than the station wagon."
problem.addConstraint(lambda truck, station_wagon: truck < station_wagon, ["truck", "station_wagon"])

# 4. "The truck is newer than the limousine."
problem.addConstraint(lambda truck, limousine: truck > limousine, ["truck", "limousine"])

# 5. "The bus is newer than the convertible."
problem.addConstraint(lambda bus, convertible: bus > convertible, ["bus", "convertible"])

# 6. "The bus is older than the tractor."
problem.addConstraint(lambda bus, tractor: bus < tractor, ["bus", "tractor"])

# 7. "The limousine is newer than the tractor."
problem.addConstraint(lambda limousine, tractor: limousine > tractor, ["limousine", "tractor"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "limousine",
    "B": "convertible",
    "C": "station_wagon",
    "D": "minivan",
    "E": "bus",
    "F": "tractor",
    "G": "truck"
}

# Find the vehicle that is third-newest (position 5)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
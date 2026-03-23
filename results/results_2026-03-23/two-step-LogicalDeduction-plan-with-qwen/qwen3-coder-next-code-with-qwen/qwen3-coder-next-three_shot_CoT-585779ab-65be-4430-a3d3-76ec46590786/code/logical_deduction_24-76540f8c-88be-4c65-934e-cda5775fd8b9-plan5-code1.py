from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["truck", "station_wagon", "motorcyle", "limousine", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The motorcyle is the second-newest" → rank = 4
problem.addConstraint(lambda motorcyle: motorcyle == 4, ["motorcyle"])

# 3. "The truck is newer than the limousine" → truck > limousine
problem.addConstraint(lambda truck, limousine: truck > limousine, ["truck", "limousine"])

# 4. "The motorcyle is older than the station wagon" → motorcyle < station_wagon
problem.addConstraint(lambda motorcyle, station_wagon: motorcyle < station_wagon, ["motorcyle", "station_wagon"])

# 5. "The limousine is newer than the hatchback" → limousine > hatchback
problem.addConstraint(lambda limousine, hatchback: limousine > hatchback, ["limousine", "hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "station_wagon",
    "C": "motorcyle",
    "D": "limousine",
    "E": "hatchback"
}

# Find which vehicle has rank 5 (newest) and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
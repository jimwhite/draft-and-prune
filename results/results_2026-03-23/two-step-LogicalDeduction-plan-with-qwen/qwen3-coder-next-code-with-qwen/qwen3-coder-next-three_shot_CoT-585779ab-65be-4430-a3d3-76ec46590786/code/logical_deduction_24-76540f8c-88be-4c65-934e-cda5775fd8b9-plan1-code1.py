from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["truck", "station_wagon", "motorcyle", "limousine", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The motorcyle is the second-newest" → rank 4
problem.addConstraint(lambda motorcyle: motorcyle == 4, ["motorcyle"])

# "The truck is newer than the limousine" → truck < limousine
problem.addConstraint(lambda truck, limousine: truck < limousine, ["truck", "limousine"])

# "The motorcyle is older than the station wagon" → station_wagon < motorcyle
problem.addConstraint(lambda station_wagon, motorcyle: station_wagon < motorcyle, ["station_wagon", "motorcyle"])

# "The limousine is newer than the hatchback" → hatchback < limousine
problem.addConstraint(lambda hatchback, limousine: hatchback < limousine, ["hatchback", "limousine"])

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

# Find which vehicle is the newest (rank 5) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
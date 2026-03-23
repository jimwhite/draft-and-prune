from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["truck", "station_wagon", "motorcycle", "limousine", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The motorcycle is the second-newest" → rank 4
problem.addConstraint(lambda motorcycle: motorcycle == 4, ["motorcycle"])

# 3. "The truck is newer than the limousine" → truck > limousine
problem.addConstraint(lambda truck, limousine: truck > limousine, ["truck", "limousine"])

# 4. "The motorcycle is older than the station wagon" → motorcycle < station_wagon
problem.addConstraint(lambda motorcycle, station_wagon: motorcycle < station_wagon, ["motorcycle", "station_wagon"])

# 5. "The limousine is newer than the hatchback" → limousine > hatchback
problem.addConstraint(lambda limousine, hatchback: limousine > hatchback, ["limousine", "hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "truck",
    "B": "station_wagon",
    "C": "motorcycle",
    "D": "limousine",
    "E": "hatchback"
}

# Find which vehicle is the newest (rank 5) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
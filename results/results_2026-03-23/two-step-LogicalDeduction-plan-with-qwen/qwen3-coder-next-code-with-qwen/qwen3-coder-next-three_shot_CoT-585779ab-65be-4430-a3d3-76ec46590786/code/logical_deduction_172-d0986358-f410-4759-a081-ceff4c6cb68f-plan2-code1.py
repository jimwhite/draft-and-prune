from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["limousine", "convertible", "station_wagon", "minivan", "bus", "tractor", "truck"]
ranks = range(1, 8)  # 1=oldest, 7=newest
problem.addVariables(vehicles, ranks)

# Add AllDifferentConstraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The minivan is the oldest"
problem.addConstraint(lambda minivan: minivan == 1, ["minivan"])

# "The truck is older than the station wagon"
problem.addConstraint(lambda truck, station_wagon: truck < station_wagon, ["truck", "station_wagon"])

# "The truck is newer than the limousine"
problem.addConstraint(lambda truck, limousine: truck > limousine, ["truck", "limousine"])

# "The bus is newer than the convertible"
problem.addConstraint(lambda bus, convertible: bus > convertible, ["bus", "convertible"])

# "The bus is older than the tractor"
problem.addConstraint(lambda bus, tractor: bus < tractor, ["bus", "tractor"])

# "The limousine is newer than the tractor"
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

# Find the vehicle that is third-newest (rank 5)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
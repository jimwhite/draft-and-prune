from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "truck", "bus", "station_wagon", "tractor", "convertible", "limousine"]
ranks = range(1, 8)  # 1 to 7
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The truck is the oldest." -> rank 1
problem.addConstraint(lambda truck: truck == 1, ["truck"])

# "The tractor is the newest." -> rank 7
problem.addConstraint(lambda tractor: tractor == 7, ["tractor"])

# "The sedan is older than the station wagon." -> sedan < station_wagon
problem.addConstraint(lambda sedan, station_wagon: sedan < station_wagon, ["sedan", "station_wagon"])

# "The station wagon is the third-newest." -> rank 5 (7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda station_wagon: station_wagon == 5, ["station_wagon"])

# "The bus is older than the convertible." -> bus < convertible
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# "The sedan is newer than the convertible." -> sedan > convertible
problem.addConstraint(lambda sedan, convertible: sedan > convertible, ["sedan", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map vehicles to choice letters
vehicle_to_choice = {
    "sedan": "A",
    "truck": "B",
    "bus": "C",
    "station_wagon": "D",
    "tractor": "E",
    "convertible": "F",
    "limousine": "G"
}

# Find the vehicle with rank 3 (third-oldest)
for solution in solutions:
    for vehicle, choice_letter in vehicle_to_choice.items():
        if solution[vehicle] == 3:
            print(choice_letter)
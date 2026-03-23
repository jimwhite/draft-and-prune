from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "convertible", "station_wagon", "bus", "motorcyle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The sedan is the second-newest." (rank 4, since 5=newest)
problem.addConstraint(lambda sedan: sedan == 4, ["sedan"])

# "The station wagon is newer than the convertible." (smaller rank = newer)
problem.addConstraint(lambda station_wagon, convertible: station_wagon < convertible, ["station_wagon", "convertible"])

# "The sedan is older than the motorcyle." (sedan has larger rank = older)
problem.addConstraint(lambda sedan, motorcyle: sedan > motorcyle, ["sedan", "motorcyle"])

# "The bus is the oldest." (rank 1)
problem.addConstraint(lambda bus: bus == 1, ["bus"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "sedan",
    "B": "convertible",
    "C": "station_wagon",
    "D": "bus",
    "E": "motorcyle"
}

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
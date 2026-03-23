from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["sedan", "convertible", "station_wagon", "bus", "motorcycle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The sedan is the second-newest." → rank = 4
problem.addConstraint(lambda sedan: sedan == 4, ["sedan"])

# 3. "The station wagon is newer than the convertible." → station_wagon < convertible
problem.addConstraint(lambda station_wagon, convertible: station_wagon < convertible, ["station_wagon", "convertible"])

# 4. "The sedan is older than the motorcycle." → sedan < motorcycle
problem.addConstraint(lambda sedan, motorcycle: sedan < motorcycle, ["sedan", "motorcycle"])

# 5. "The bus is the oldest." → bus == 1
problem.addConstraint(lambda bus: bus == 1, ["bus"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "sedan",
    "B": "convertible",
    "C": "station_wagon",
    "D": "bus",
    "E": "motorcycle"
}

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (ranks: 1=oldest, 5=newest)
vehicles = ["station_wagon", "sedan", "tractor", "motorcycle", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different ranks
problem.addConstraint(AllDifferentConstraint())

# The tractor is newer than the motorcycle (higher rank number)
problem.addConstraint(lambda tractor, motorcycle: tractor > motorcycle, ("tractor", "motorcycle"))

# The motorcycle is newer than the sedan (higher rank number)
problem.addConstraint(lambda motorcycle, sedan: motorcycle > sedan, ("motorcycle", "sedan"))

# The limousine is the oldest (rank 1)
problem.addConstraint(lambda limousine: limousine == 1, ("limousine",))

# The station wagon is the newest (rank 5)
problem.addConstraint(lambda station_wagon: station_wagon == 5, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "station_wagon",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcycle",
    "E": "limousine"
}

# Find the vehicle with rank 4 (second-newest) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
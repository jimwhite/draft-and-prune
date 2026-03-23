from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["station_wagon", "sedan", "tractor", "motorcycle", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the motorcycle" → tractor > motorcycle
problem.addConstraint(lambda tractor, motorcycle: tractor > motorcycle, ("tractor", "motorcycle"))

# "The motorcycle is newer than the sedan" → motorcycle > sedan
problem.addConstraint(lambda motorcycle, sedan: motorcycle > sedan, ("motorcycle", "sedan"))

# "The limousine is the oldest" → limousine == 1
problem.addConstraint(lambda limousine: limousine == 1, ("limousine",))

# "The station wagon is the newest" → station_wagon == 5
problem.addConstraint(lambda station_wagon: station_wagon == 5, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "station_wagon",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcycle",
    "E": "limousine"
}

# Find the vehicle that is second-newest (position 4)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
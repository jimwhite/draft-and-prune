from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["station_wagon", "sedan", "tractor", "motorcycle", "limousine"]
positions = range(1, 6)
problem.addVariables(vehicles, positions)

# Add constraints
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

# Find which vehicle is oldest (position 1) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
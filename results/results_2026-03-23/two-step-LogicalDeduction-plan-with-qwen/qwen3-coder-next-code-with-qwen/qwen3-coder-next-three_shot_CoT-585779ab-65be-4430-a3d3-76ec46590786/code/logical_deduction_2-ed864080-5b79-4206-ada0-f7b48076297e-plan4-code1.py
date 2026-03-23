from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["station_wagon", "sedan", "tractor", "motorcycle", "limousine"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the motorcycle" → tractor rank > motorcycle rank
problem.addConstraint(lambda t, m: t > m, ("tractor", "motorcycle"))

# "The motorcycle is newer than the sedan" → motorcycle rank > sedan rank
problem.addConstraint(lambda m, s: m > s, ("motorcycle", "sedan"))

# "The limousine is the oldest" → limousine rank = 1
problem.addConstraint(lambda l: l == 1, ("limousine",))

# "The station wagon is the newest" → station_wagon rank = 5
problem.addConstraint(lambda st: st == 5, ("station_wagon",))

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

# Find which vehicle has rank 1 (oldest) and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
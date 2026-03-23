from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# The minivan is older than the sedan → minivan < sedan
problem.addConstraint(lambda minivan, sedan: minivan < sedan, ("minivan", "sedan"))

# The tractor is older than the hatchback → tractor < hatchback
problem.addConstraint(lambda tractor, hatchback: tractor < hatchback, ("tractor", "hatchback"))

# The minivan is the third-newest → position 3 (since newest=5, second-newest=4, third-newest=3)
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# The station wagon is the second-newest → position 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "tractor",
    "B": "station_wagon",
    "C": "minivan",
    "D": "sedan",
    "E": "hatchback"
}

# Find which vehicle has rank 3 (third-newest) and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
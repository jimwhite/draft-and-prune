from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "bus", "motorcycle", "minivan"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the motorcycle" → minivan < motorcycle
problem.addConstraint(lambda minivan, motorcycle: minivan < motorcycle, ("minivan", "motorcycle"))

# "The bus is the newest" → bus == 5
problem.addConstraint(lambda bus: bus == 5, ("bus",))

# "The tractor is the third-newest" → tractor == 3
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# "The station wagon is the second-oldest" → station_wagon == 2
problem.addConstraint(lambda station_wagon: station_wagon == 2, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the newest (position 5)
# From constraints, bus == 5, so we expect choice C to be correct
choices = {
    "A": "tractor",
    "B": "station_wagon",
    "C": "bus",
    "D": "motorcycle",
    "E": "minivan"
}

# Find which vehicle is at position 5 (newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
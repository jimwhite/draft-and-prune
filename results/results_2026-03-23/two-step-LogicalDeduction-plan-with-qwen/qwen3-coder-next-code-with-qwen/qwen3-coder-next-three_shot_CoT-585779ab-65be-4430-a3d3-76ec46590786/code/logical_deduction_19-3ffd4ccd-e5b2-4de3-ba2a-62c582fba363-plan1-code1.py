from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "bus", "motorcycle", "minivan"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the motorcycle"
problem.addConstraint(lambda minivan, motorcycle: minivan < motorcycle, ("minivan", "motorcycle"))

# "The bus is the newest"
problem.addConstraint(lambda bus: bus == 5, ("bus",))

# "The tractor is the third-newest" (positions: 1=oldest, 2, 3=third-newest, 4, 5=newest)
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# "The station wagon is the second-oldest" (positions: 1=oldest, 2=second-oldest, ...)
problem.addConstraint(lambda station_wagon: station_wagon == 2, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "tractor",
    "B": "station_wagon",
    "C": "bus",
    "D": "motorcycle",
    "E": "minivan"
}

# Find which vehicle is the newest (position 5)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
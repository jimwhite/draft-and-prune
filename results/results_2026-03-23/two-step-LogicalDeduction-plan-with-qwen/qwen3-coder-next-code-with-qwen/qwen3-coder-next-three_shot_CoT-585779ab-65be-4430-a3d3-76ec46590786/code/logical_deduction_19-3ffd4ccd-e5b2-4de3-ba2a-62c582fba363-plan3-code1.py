from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["tractor", "station_wagon", "bus", "motorcycle", "minivan"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is older than the motorcycle" → minivan < motorcycle
problem.addConstraint(lambda minivan, motorcycle: minivan < motorcycle, ("minivan", "motorcycle"))

# 3. "The bus is the newest" → bus == 5
problem.addConstraint(lambda bus: bus == 5, ("bus",))

# 4. "The tractor is the third-newest" → rank 3 (since 5=newest, 4=second-newest, 3=third-newest)
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# 5. "The station wagon is the second-oldest" → rank 2 (since 1=oldest, 2=second-oldest)
problem.addConstraint(lambda station_wagon: station_wagon == 2, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "tractor",
    "B": "station_wagon",
    "C": "bus",
    "D": "motorcycle",
    "E": "minivan"
}

# Find which vehicle is the newest (rank 5) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
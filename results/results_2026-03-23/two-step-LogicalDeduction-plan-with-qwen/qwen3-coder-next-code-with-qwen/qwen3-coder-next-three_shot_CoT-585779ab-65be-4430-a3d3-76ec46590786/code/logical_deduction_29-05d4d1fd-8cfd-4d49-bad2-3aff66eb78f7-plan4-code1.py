from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["truck", "station_wagon", "motorcycle", "convertible", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The convertible is newer than the truck" → convertible > truck
problem.addConstraint(lambda convertible, truck: convertible > truck, ("convertible", "truck"))

# 3. "The station wagon is newer than the hatchback" → station_wagon > hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon > hatchback, ("station_wagon", "hatchback"))

# 4. "The convertible is older than the hatchback" → convertible < hatchback
problem.addConstraint(lambda convertible, hatchback: convertible < hatchback, ("convertible", "hatchback"))

# 5. "The station wagon is the second-newest" → station_wagon == 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for comparison
choices = {
    "A": "truck",
    "B": "station_wagon",
    "C": "motorcycle",
    "D": "convertible",
    "E": "hatchback"
}

# Find which vehicle has rank 4 (second-newest) and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
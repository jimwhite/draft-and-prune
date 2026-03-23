from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["tractor", "truck", "bus", "minivan", "convertible"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The bus is newer than the tractor" → bus > tractor
problem.addConstraint(lambda tractor, bus: bus > tractor, ("tractor", "bus"))

# 3. "The convertible is older than the tractor" → convertible < tractor
problem.addConstraint(lambda convertible, tractor: convertible < tractor, ("convertible", "tractor"))

# 4. "The truck is the second-newest" → truck == 4
problem.addConstraint(lambda truck: truck == 4, ("truck",))

# 5. "The minivan is older than the convertible" → minivan < convertible
problem.addConstraint(lambda minivan, convertible: minivan < convertible, ("minivan", "convertible"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for the question about third-newest (rank 3)
choices = {
    "A": "tractor",
    "B": "truck",
    "C": "bus",
    "D": "minivan",
    "E": "convertible"
}

# Find which vehicle has rank 3 (third-newest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
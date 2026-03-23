from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "truck", "bus", "minivan", "convertible"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add age-based constraints
# "The bus is newer than the tractor" -> bus > tractor
problem.addConstraint(lambda tractor, bus: tractor < bus, ("tractor", "bus"))

# "The convertible is older than the tractor" -> convertible < tractor
problem.addConstraint(lambda convertible, tractor: convertible < tractor, ("convertible", "tractor"))

# "The truck is the second-newest" -> truck == 4 (since 5 is newest)
problem.addConstraint(lambda truck: truck == 4, ("truck",))

# "The minivan is older than the convertible" -> minivan < convertible
problem.addConstraint(lambda minivan, convertible: minivan < convertible, ("minivan", "convertible"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "tractor",
    "B": "truck",
    "C": "bus",
    "D": "minivan",
    "E": "convertible"
}

# Find which vehicle is third-newest (rank 3) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
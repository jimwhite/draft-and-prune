from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "truck", "bus", "minivan", "convertible"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The bus is newer than the tractor" -> bus > tractor
problem.addConstraint(lambda bus, tractor: bus > tractor, ("bus", "tractor"))

# "The convertible is older than the tractor" -> convertible < tractor
problem.addConstraint(lambda convertible, tractor: convertible < tractor, ("convertible", "tractor"))

# "The truck is the second-newest" -> truck == 4
problem.addConstraint(lambda truck: truck == 4, ("truck",))

# "The minivan is older than the convertible" -> minivan < convertible
problem.addConstraint(lambda minivan, convertible: minivan < convertible, ("minivan", "convertible"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "tractor",
    "B": "truck",
    "C": "bus",
    "D": "minivan",
    "E": "convertible"
}

# Find the vehicle that is oldest (rank 1) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
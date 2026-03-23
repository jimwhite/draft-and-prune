from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "bus", "limousine", "truck", "convertible", "tractor", "motorcyle"]
ranks = range(1, 8)  # 1=oldest, 7=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The limousine is older than the minivan"
problem.addConstraint(lambda limousine, minivan: limousine < minivan, ("limousine", "minivan"))

# "The tractor is older than the limousine"
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The bus is the newest"
problem.addConstraint(lambda bus: bus == 7, ("bus",))

# "The truck is the third-newest" (newest=7, so third-newest=5)
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# "The motorcyle is the fourth-newest" (fourth-newest=4)
problem.addConstraint(lambda motorcyle: motorcyle == 4, ("motorcyle",))

# "The convertible is older than the tractor"
problem.addConstraint(lambda convertible, tractor: convertible < tractor, ("convertible", "tractor"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "minivan",
    "B": "bus",
    "C": "limousine",
    "D": "truck",
    "E": "convertible",
    "F": "tractor",
    "G": "motorcyle"
}

# Find which vehicle has rank 3 (third-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
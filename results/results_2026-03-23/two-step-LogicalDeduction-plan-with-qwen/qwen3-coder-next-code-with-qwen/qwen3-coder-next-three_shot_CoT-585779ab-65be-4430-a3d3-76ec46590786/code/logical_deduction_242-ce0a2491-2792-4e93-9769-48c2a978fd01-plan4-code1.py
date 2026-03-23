from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three vehicles) and domain (age ranks: 1=oldest, 3=newest)
vehicles = ["minivan", "bus", "sedan"]
ranks = range(1, 4)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is newer than the sedan" => minivan's rank > sedan's rank
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# 3. "The minivan is older than the bus" => minivan's rank < bus's rank
problem.addConstraint(lambda minivan, bus: minivan < bus, ("minivan", "bus"))

# Find the unique solution
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "minivan",
    "B": "bus",
    "C": "sedan"
}

# Find which vehicle has rank 1 (oldest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
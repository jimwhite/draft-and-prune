from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the three vehicles) and domain (age ranks 1 to 3, where 1=oldest, 3=newest)
vehicles = ["bus", "sedan", "truck"]
ranks = range(1, 4)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The truck is older than the bus." (truck's rank < bus's rank)
problem.addConstraint(lambda truck, bus: truck < bus, ("truck", "bus"))

# 3. "The bus is older than the sedan." (bus's rank < sedan's rank)
problem.addConstraint(lambda bus, sedan: bus < sedan, ("bus", "sedan"))

# Find the unique solution
solutions = problem.getSolutions()

# Map choice letters to vehicle names based on the question's choices
choices = {
    "A": "bus",
    "B": "sedan",
    "C": "truck"
}

# Find which vehicle has rank 3 (newest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
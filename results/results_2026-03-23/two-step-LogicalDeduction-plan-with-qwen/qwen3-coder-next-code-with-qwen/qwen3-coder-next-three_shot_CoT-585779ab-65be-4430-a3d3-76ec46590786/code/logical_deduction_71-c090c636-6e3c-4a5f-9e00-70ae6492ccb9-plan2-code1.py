from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranking)
# 1 = newest, 5 = oldest
vehicles = ["convertible", "sedan", "tractor", "minivan", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is newer than the minivan" → tractor < minivan
problem.addConstraint(lambda tractor, minivan: tractor < minivan, ("tractor", "minivan"))

# 3. "The tractor is older than the limousine" → tractor > limousine
problem.addConstraint(lambda tractor, limousine: tractor > limousine, ("tractor", "limousine"))

# 4. "The convertible is older than the sedan" → convertible > sedan
problem.addConstraint(lambda convertible, sedan: convertible > sedan, ("convertible", "sedan"))

# 5. "The convertible is the second-newest" → convertible == 2
problem.addConstraint(lambda convertible: convertible == 2, ("convertible",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for "third-newest" (position 3)
choices = {
    "A": "convertible",
    "B": "sedan",
    "C": "tractor",
    "D": "minivan",
    "E": "limousine"
}

# Find which vehicle has rank 3 (third-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
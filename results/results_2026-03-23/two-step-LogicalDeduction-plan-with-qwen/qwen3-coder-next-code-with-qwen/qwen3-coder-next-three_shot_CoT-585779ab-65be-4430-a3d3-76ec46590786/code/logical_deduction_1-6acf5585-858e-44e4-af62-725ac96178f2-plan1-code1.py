from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "sedan", "tractor", "minivan", "limousine"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the minivan" → minivan < tractor
problem.addConstraint(lambda minivan, tractor: minivan < tractor, ("minivan", "tractor"))

# "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The convertible is older than the sedan" → convertible < sedan
problem.addConstraint(lambda convertible, sedan: convertible < sedan, ("convertible", "sedan"))

# "The convertible is the second-newest" → convertible == 4
problem.addConstraint(lambda convertible: convertible == 4, ("convertible",))

# Solve the problem
solutions = problem.getSolutions()

# Check which choice is true by verifying the position of each vehicle at rank 4
choices = {
    "A": "convertible",
    "B": "sedan",
    "C": "tractor",
    "D": "minivan",
    "E": "limousine"
}

# Find which vehicle is at position 4 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
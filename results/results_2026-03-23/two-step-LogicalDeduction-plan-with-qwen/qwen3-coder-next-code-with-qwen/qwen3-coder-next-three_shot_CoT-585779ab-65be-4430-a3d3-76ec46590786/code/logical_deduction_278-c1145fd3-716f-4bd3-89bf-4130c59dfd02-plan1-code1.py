from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "tractor", "hatchback"]
ranks = range(1, 4)  # 1=newest, 2=second-newest, 3=oldest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is older than the convertible" means hatchback's rank > convertible's rank
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ("hatchback", "convertible"))

# "The tractor is the newest" means tractor's rank = 1
problem.addConstraint(lambda tractor: tractor == 1, ("tractor",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "convertible",
    "B": "tractor",
    "C": "hatchback"
}

# Find which vehicle has rank 2 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
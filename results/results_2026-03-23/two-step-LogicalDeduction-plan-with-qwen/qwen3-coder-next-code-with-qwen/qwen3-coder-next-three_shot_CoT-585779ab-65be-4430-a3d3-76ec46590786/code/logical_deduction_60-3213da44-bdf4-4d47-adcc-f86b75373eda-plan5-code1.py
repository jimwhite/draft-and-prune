from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["bus", "truck", "motorcyle", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The sedan is the second-oldest."
problem.addConstraint(lambda sedan: sedan == 2, ["sedan"])

# "The hatchback is newer than the motorcyle."
problem.addConstraint(lambda hatchback, motorcyle: hatchback > motorcyle, ["hatchback", "motorcyle"])

# "The motorcyle is newer than the sedan."
problem.addConstraint(lambda motorcyle, sedan: motorcyle > sedan, ["motorcyle", "sedan"])

# "The hatchback is older than the truck."
problem.addConstraint(lambda hatchback, truck: hatchback < truck, ["hatchback", "truck"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "bus",
    "B": "truck",
    "C": "motorcyle",
    "D": "sedan",
    "E": "hatchback"
}

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
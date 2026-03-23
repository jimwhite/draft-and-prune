from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["bus", "truck", "motorcyle", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add AllDifferentConstraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The sedan is the second-oldest" -> rank 2
problem.addConstraint(lambda sedan: sedan == 2, ["sedan"])

# "The hatchback is newer than the motorcyle" -> hatchback > motorcyle
problem.addConstraint(lambda hatchback, motorcyle: hatchback > motorcyle, ["hatchback", "motorcyle"])

# "The motorcyle is newer than the sedan" -> motorcyle > sedan
problem.addConstraint(lambda motorcyle, sedan: motorcyle > sedan, ["motorcyle", "sedan"])

# "The hatchback is older than the truck" -> hatchback < truck
problem.addConstraint(lambda hatchback, truck: hatchback < truck, ["hatchback", "truck"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know from constraints that sedan == 2, the second-oldest is the sedan
# Check against choices to confirm
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
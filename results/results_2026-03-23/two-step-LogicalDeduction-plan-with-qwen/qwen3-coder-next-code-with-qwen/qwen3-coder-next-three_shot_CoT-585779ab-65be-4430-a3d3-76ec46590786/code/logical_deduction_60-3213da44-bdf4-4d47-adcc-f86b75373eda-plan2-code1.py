from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["bus", "truck", "motorcyle", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The sedan is the second-oldest" → rank = 2
problem.addConstraint(lambda sedan: sedan == 2, ["sedan"])

# 3. "The hatchback is newer than the motorcyle" → hatchback > motorcyle
problem.addConstraint(lambda hatchback, motorcyle: hatchback > motorcyle, ["hatchback", "motorcyle"])

# 4. "The motorcyle is newer than the sedan" → motorcyle > sedan
problem.addConstraint(lambda motorcyle, sedan: motorcyle > sedan, ["motorcyle", "sedan"])

# 5. "The hatchback is older than the truck" → hatchback < truck
problem.addConstraint(lambda hatchback, truck: hatchback < truck, ["hatchback", "truck"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names as per the choices
choices = {
    "A": "bus",
    "B": "truck",
    "C": "motorcyle",
    "D": "sedan",
    "E": "hatchback"
}

# Find which vehicle has rank 2 (second-oldest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
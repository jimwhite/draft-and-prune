from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcyle"]
positions = range(1, 6)
problem.addVariables(vehicles, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is newer than the convertible" → hatchback > convertible
problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ["hatchback", "convertible"])

# "The bus is newer than the hatchback" → bus > hatchback
problem.addConstraint(lambda bus, hatchback: bus > hatchback, ["bus", "hatchback"])

# "The bus is older than the motorcyle" → bus < motorcyle
problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ["bus", "motorcyle"])

# "The minivan is the newest" → minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ["minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "minivan",
    "B": "hatchback",
    "C": "bus",
    "D": "convertible",
    "E": "motorcyle"
}

# Find which vehicle is at position 5 (newest)
for solution in solutions:
    for letter, vehicle in choices.items():
        if solution[vehicle] == 5:
            print(letter)
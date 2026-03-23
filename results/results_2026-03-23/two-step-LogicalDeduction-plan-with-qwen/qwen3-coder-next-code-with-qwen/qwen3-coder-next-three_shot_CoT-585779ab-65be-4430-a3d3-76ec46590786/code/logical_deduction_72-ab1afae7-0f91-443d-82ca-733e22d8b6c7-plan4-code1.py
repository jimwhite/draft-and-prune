from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "convertible", "tractor", "truck", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The tractor is newer than the hatchback" → tractor > hatchback
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ["hatchback", "tractor"])

# "The limousine is the second-newest" → limousine == 4
problem.addConstraint(lambda limousine: limousine == 4, ["limousine"])

# "The truck is older than the hatchback" → truck < hatchback
problem.addConstraint(lambda truck, hatchback: truck < hatchback, ["truck", "hatchback"])

# "The convertible is the second-oldest" → convertible == 2
problem.addConstraint(lambda convertible: convertible == 2, ["convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "hatchback",
    "B": "convertible",
    "C": "tractor",
    "D": "truck",
    "E": "limousine"
}

# Find which vehicle is at position 4 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
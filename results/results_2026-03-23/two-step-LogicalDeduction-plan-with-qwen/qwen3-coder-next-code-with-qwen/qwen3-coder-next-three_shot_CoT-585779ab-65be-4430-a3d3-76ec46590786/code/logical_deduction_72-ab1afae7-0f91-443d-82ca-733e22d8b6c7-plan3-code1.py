from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["hatchback", "convertible", "tractor", "truck", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

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

# Map choices to vehicles
choices = {
    "A": "hatchback",
    "B": "convertible",
    "C": "tractor",
    "D": "truck",
    "E": "limousine"
}

# Find which vehicle is second-newest (rank 4) and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
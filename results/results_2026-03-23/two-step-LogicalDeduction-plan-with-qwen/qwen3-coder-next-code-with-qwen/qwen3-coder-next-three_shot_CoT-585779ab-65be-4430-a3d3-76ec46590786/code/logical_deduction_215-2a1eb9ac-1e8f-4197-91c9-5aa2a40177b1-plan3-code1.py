from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles)
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcyle", "hatchback", "sedan"]

# Define domain: ranks 1 to 7, where 1 = oldest and 7 = newest
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles must have unique ranks
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is the fourth-newest" → rank = 4
problem.addConstraint(lambda hatchback: hatchback == 4, ["hatchback"])

# "The limousine is older than the motorcyle" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ["limousine", "motorcyle"])

# "The truck is newer than the motorcyle" → truck > motorcyle
problem.addConstraint(lambda truck, motorcyle: truck > motorcyle, ["truck", "motorcyle"])

# "The sedan is the second-newest" → rank = 6
problem.addConstraint(lambda sedan: sedan == 6, ["sedan"])

# "The tractor is newer than the convertible" → tractor > convertible
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ["tractor", "convertible"])

# "The hatchback is older than the convertible" → hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks for the third-newest vehicle, which corresponds to rank 5
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "tractor",
    "D": "limousine",
    "E": "motorcyle",
    "F": "hatchback",
    "G": "sedan"
}

# Find which vehicle has rank 5 and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
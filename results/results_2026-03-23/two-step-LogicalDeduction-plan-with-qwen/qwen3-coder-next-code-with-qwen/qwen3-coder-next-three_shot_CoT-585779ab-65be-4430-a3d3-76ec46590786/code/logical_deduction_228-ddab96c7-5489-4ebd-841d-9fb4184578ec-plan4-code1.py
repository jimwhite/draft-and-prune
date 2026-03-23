from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcyle", "hatchback", "sedan"]

# Define the domain: ranks 1 to 7, where 1 = oldest and 7 = newest
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have distinct ranks
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is the fourth-newest" → rank = 4 (since 1st-newest=7, 2nd-newest=6, 3rd-newest=5, 4th-newest=4)
problem.addConstraint(lambda hatchback: hatchback == 4, ["hatchback"])

# "The limousine is older than the motorcyle" → limousine rank < motorcyle rank
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ["limousine", "motorcyle"])

# "The truck is newer than the motorcyle" → truck rank > motorcyle rank
problem.addConstraint(lambda truck, motorcyle: truck > motorcyle, ["truck", "motorcyle"])

# "The sedan is the second-newest" → rank = 6
problem.addConstraint(lambda sedan: sedan == 6, ["sedan"])

# "The tractor is newer than the convertible" → tractor rank > convertible rank
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ["tractor", "convertible"])

# "The hatchback is older than the convertible" → hatchback rank < convertible rank
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "tractor",
    "D": "limousine",
    "E": "motorcyle",
    "F": "hatchback",
    "G": "sedan"
}

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcyle", "hatchback", "sedan"]

# Define the domain: positions 1 to 7, where 1 = oldest and 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem description
# 1. All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The hatchback is the fourth-newest" → rank = 4
problem.addConstraint(lambda hatchback: hatchback == 4, ["hatchback"])

# 3. "The limousine is older than the motorcyle" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ["limousine", "motorcyle"])

# 4. "The truck is newer than the motorcyle" → truck > motorcyle
problem.addConstraint(lambda truck, motorcyle: truck > motorcyle, ["truck", "motorcyle"])

# 5. "The sedan is the second-newest" → rank = 6
problem.addConstraint(lambda sedan: sedan == 6, ["sedan"])

# 6. "The tractor is newer than the convertible" → tractor > convertible
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ["tractor", "convertible"])

# 7. "The hatchback is older than the convertible" → hatchback < convertible
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
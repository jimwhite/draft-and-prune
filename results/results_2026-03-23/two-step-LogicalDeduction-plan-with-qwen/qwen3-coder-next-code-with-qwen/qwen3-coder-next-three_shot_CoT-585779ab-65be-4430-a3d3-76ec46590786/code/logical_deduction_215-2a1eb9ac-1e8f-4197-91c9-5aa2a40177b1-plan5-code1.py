from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcyle", "hatchback", "sedan"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The hatchback is the fourth-newest" → rank = 4
problem.addConstraint(lambda hatchback: hatchback == 4, ["hatchback"])

# 2. "The limousine is older than the motorcyle" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ["limousine", "motorcyle"])

# 3. "The truck is newer than the motorcyle" → truck > motorcyle
problem.addConstraint(lambda truck, motorcyle: truck > motorcyle, ["truck", "motorcyle"])

# 4. "The sedan is the second-newest" → rank = 6
problem.addConstraint(lambda sedan: sedan == 6, ["sedan"])

# 5. "The tractor is newer than the convertible" → tractor > convertible
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ["tractor", "convertible"])

# 6. "The hatchback is older than the convertible" → hatchback < convertible (4 < convertible_rank)
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for third-newest (rank 5)
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "tractor",
    "D": "limousine",
    "E": "motorcyle",
    "F": "hatchback",
    "G": "sedan"
}

# Find which vehicle has rank 5 (third-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
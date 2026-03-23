from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (positions 1 to 7, where 1=oldest, 7=newest)
vehicles = ["convertible", "truck", "tractor", "limousine", "motorcyle", "hatchback", "sedan"]
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements
# "The hatchback is the fourth-newest" → position 4 (since newest=7, fourth-newest = 7-3 = 4)
problem.addConstraint(lambda hatchback: hatchback == 4, ["hatchback"])

# "The limousine is older than the motorcyle" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ["limousine", "motorcyle"])

# "The truck is newer than the motorcyle" → truck > motorcyle
problem.addConstraint(lambda truck, motorcyle: truck > motorcyle, ["truck", "motorcyle"])

# "The sedan is the second-newest" → position 6 (7-1 = 6)
problem.addConstraint(lambda sedan: sedan == 6, ["sedan"])

# "The tractor is newer than the convertible" → tractor > convertible
problem.addConstraint(lambda tractor, convertible: tractor > convertible, ["tractor", "convertible"])

# "The hatchback is older than the convertible" → hatchback < convertible
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ["hatchback", "convertible"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks for the third-newest vehicle, which corresponds to position 5
# (positions: 1=oldest, 2=second-oldest, 3=third-oldest, 4=fourth-newest, 5=third-newest, 6=second-newest, 7=newest)
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "tractor",
    "D": "limousine",
    "E": "motorcyle",
    "F": "hatchback",
    "G": "sedan"
}

# Find the vehicle at position 5 and print its corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
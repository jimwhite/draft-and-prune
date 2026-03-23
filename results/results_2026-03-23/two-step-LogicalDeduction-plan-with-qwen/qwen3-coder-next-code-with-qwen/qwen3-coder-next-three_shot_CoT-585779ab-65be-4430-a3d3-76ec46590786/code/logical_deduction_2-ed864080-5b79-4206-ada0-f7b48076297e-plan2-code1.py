from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["station_wagon", "sedan", "tractor", "motorcyle", "limousine"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the motorcyle" -> tractor > motorcyle
problem.addConstraint(lambda tractor, motorcyle: tractor > motorcyle, ("tractor", "motorcyle"))

# "The motorcyle is newer than the sedan" -> motorcyle > sedan
problem.addConstraint(lambda motorcyle, sedan: motorcyle > sedan, ("motorcyle", "sedan"))

# "The limousine is the oldest" -> limousine == 1
problem.addConstraint(lambda limousine: limousine == 1, ("limousine",))

# "The station wagon is the newest" -> station_wagon == 5
problem.addConstraint(lambda station_wagon: station_wagon == 5, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "station_wagon",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcyle",
    "E": "limousine"
}

# Find which vehicle is the oldest (rank 1) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
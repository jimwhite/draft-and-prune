from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the five vehicles) and their domain (age rank)
vehicles = ["station_wagon", "sedan", "tractor", "motorcyle", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is newer than the motorcyle." (motorcyle is older, so rank < tractor)
problem.addConstraint(lambda motorcyle, tractor: motorcyle < tractor, ("motorcyle", "tractor"))

# 3. "The motorcyle is newer than the sedan." (sedan is older, so rank < motorcyle)
problem.addConstraint(lambda sedan, motorcyle: sedan < motorcyle, ("sedan", "motorcyle"))

# 4. "The limousine is the oldest." (rank = 1)
problem.addConstraint(lambda limousine: limousine == 1, ("limousine",))

# 5. "The station wagon is the newest." (rank = 5)
problem.addConstraint(lambda station_wagon: station_wagon == 5, ("station_wagon",))

# Find the unique solution
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "station_wagon",
    "B": "sedan",
    "C": "tractor",
    "D": "motorcyle",
    "E": "limousine"
}

# Find which vehicle is the oldest (rank = 1) and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
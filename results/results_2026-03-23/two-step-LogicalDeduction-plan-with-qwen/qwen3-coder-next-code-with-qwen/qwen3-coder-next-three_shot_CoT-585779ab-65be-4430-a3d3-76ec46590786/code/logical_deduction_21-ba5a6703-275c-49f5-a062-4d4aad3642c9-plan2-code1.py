from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the five vehicles) and the domain (their age rank)
# Ranks: 1 = oldest, 5 = newest
vehicles = ["truck", "motorcyle", "limousine", "station_wagon", "sedan"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The limousine is older than the truck." (limousine's rank < truck's rank)
problem.addConstraint(lambda limousine, truck: limousine < truck, ("limousine", "truck"))

# 3. "The sedan is newer than the motorcyle." (motorcyle's rank < sedan's rank)
problem.addConstraint(lambda motorcyle, sedan: motorcyle < sedan, ("motorcyle", "sedan"))

# 4. "The station wagon is the oldest." (station_wagon's rank = 1)
problem.addConstraint(lambda station_wagon: station_wagon == 1, ("station_wagon",))

# 5. "The limousine is newer than the sedan." (sedan's rank < limousine's rank)
problem.addConstraint(lambda sedan, limousine: sedan < limousine, ("sedan", "limousine"))

# Find the unique solution to the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the "second-oldest" (rank = 2)
choices = {
    "A": "truck",
    "B": "motorcyle",
    "C": "limousine",
    "D": "station_wagon",
    "E": "sedan"
}

# Check the solution to find the vehicle with rank 2 and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
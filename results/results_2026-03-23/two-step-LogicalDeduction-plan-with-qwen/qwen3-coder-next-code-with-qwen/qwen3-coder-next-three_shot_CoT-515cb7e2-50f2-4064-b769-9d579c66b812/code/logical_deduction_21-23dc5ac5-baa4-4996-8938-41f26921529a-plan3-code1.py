from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["truck", "motorcyle", "limousine", "station_wagon", "sedan"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The limousine is older than the truck" → limousine rank < truck rank
problem.addConstraint(lambda l, t: l < t, ("limousine", "truck"))

# 3. "The sedan is newer than the motorcyle" → motorcyle rank < sedan rank
problem.addConstraint(lambda m, s: m < s, ("motorcyle", "sedan"))

# 4. "The station wagon is the oldest" → station_wagon rank = 1
problem.addConstraint(lambda sw: sw == 1, ("station_wagon",))

# 5. "The limousine is newer than the sedan" → limousine rank > sedan rank
problem.addConstraint(lambda l, s: l > s, ("limousine", "sedan"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for second-oldest (rank 2)
choices = {
    "A": "truck",
    "B": "motorcyle",
    "C": "limousine",
    "D": "station_wagon",
    "E": "sedan"
}

# Find which vehicle has rank 2 and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
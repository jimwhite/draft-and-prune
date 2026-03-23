from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["truck", "motorcyle", "limousine", "station_wagon", "sedan"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The limousine is older than the truck" → limousine < truck
problem.addConstraint(lambda limousine, truck: limousine < truck, ("limousine", "truck"))

# 3. "The sedan is newer than the motorcyle" → motorcyle < sedan
problem.addConstraint(lambda motorcyle, sedan: motorcyle < sedan, ("motorcyle", "sedan"))

# 4. "The station wagon is the oldest" → station_wagon == 1
problem.addConstraint(lambda station_wagon: station_wagon == 1, ("station_wagon",))

# 5. "The limousine is newer than the sedan" → sedan < limousine
problem.addConstraint(lambda sedan, limousine: sedan < limousine, ("sedan", "limousine"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "motorcyle",
    "C": "limousine",
    "D": "station_wagon",
    "E": "sedan"
}

# Find which vehicle has rank 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
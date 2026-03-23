from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["truck", "motorcyle", "sedan", "minivan", "station_wagon", "hatchback", "tractor"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferentConstraint to ensure unique positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The hatchback is newer than the truck" → hatchback > truck
problem.addConstraint(lambda hatchback, truck: hatchback > truck, ("hatchback", "truck"))

# 2. "The sedan is the third-newest" → sedan == 5
problem.addConstraint(lambda sedan: sedan == 5, ("sedan",))

# 3. "The station wagon is the newest" → station_wagon == 7
problem.addConstraint(lambda station_wagon: station_wagon == 7, ("station_wagon",))

# 4. "The motorcyle is older than the truck" → motorcyle < truck
problem.addConstraint(lambda motorcyle, truck: motorcyle < truck, ("motorcyle", "truck"))

# 5. "The minivan is newer than the sedan" → minivan > sedan
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# 6. "The tractor is the third-oldest" → tractor == 3
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "motorcyle",
    "C": "sedan",
    "D": "minivan",
    "E": "station_wagon",
    "F": "hatchback",
    "G": "tractor"
}

# Find the vehicle with rank 4 (fourth-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
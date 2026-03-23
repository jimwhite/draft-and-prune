from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1=oldest to 7=newest)
vehicles = ["truck", "motorcyle", "sedan", "minivan", "station_wagon", "hatchback", "tractor"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hatchback is newer than the truck" → hatchback > truck
problem.addConstraint(lambda hatchback, truck: hatchback > truck, ("hatchback", "truck"))

# "The sedan is the third-newest" → sedan == 5 (since newest=7, so 7-3+1=5)
problem.addConstraint(lambda sedan: sedan == 5, ("sedan",))

# "The station wagon is the newest" → station_wagon == 7
problem.addConstraint(lambda station_wagon: station_wagon == 7, ("station_wagon",))

# "The motorcyle is older than the truck" → motorcyle < truck
problem.addConstraint(lambda motorcyle, truck: motorcyle < truck, ("motorcyle", "truck"))

# "The minivan is newer than the sedan" → minivan > sedan (i.e., minivan > 5)
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# "The tractor is the third-oldest" → tractor == 3 (oldest=1, second-oldest=2, third-oldest=3)
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# Solve the problem
solutions = problem.getSolutions()

# The fourth-newest corresponds to rank 4 (since newest=7, so 7-4+1=4)
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

# Find which vehicle has rank 4 and print the corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
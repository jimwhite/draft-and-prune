from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (positions 1 to 7, where 1=oldest, 7=newest)
vehicles = ["truck", "motorcycle", "sedan", "minivan", "station_wagon", "hatchback", "tractor"]
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The hatchback is newer than the truck" → hatchback > truck
problem.addConstraint(lambda hatchback, truck: hatchback > truck, ("hatchback", "truck"))

# "The sedan is the third-newest" → sedan == 5 (since 7=newest, 6=2nd-newest, 5=3rd-newest)
problem.addConstraint(lambda sedan: sedan == 5, ("sedan",))

# "The station wagon is the newest" → station_wagon == 7
problem.addConstraint(lambda station_wagon: station_wagon == 7, ("station_wagon",))

# "The motorcycle is older than the truck" → motorcycle < truck
problem.addConstraint(lambda motorcycle, truck: motorcycle < truck, ("motorcycle", "truck"))

# "The minivan is newer than the sedan" → minivan > sedan (i.e., minivan > 5)
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# "The tractor is the third-oldest" → tractor == 3 (since 1=oldest, 2=2nd-oldest, 3=3rd-oldest)
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "truck",
    "B": "motorcycle", 
    "C": "sedan",
    "D": "minivan",
    "E": "station_wagon",
    "F": "hatchback",
    "G": "tractor"
}

# Find the vehicle that is fourth-newest (position 4 in our numbering)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
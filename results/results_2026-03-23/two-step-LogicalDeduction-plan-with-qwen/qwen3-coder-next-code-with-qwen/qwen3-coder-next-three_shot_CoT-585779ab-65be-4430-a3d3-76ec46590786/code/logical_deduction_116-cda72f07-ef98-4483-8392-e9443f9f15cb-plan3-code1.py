from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["truck", "motorcycle", "sedan", "minivan", "station_wagon", "hatchback", "tractor"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The hatchback is newer than the truck" → hatchback > truck
problem.addConstraint(lambda hatchback, truck: hatchback > truck, ("hatchback", "truck"))

# 3. "The sedan is the third-newest" → sedan == 5
problem.addConstraint(lambda sedan: sedan == 5, ("sedan",))

# 4. "The station wagon is the newest" → station_wagon == 7
problem.addConstraint(lambda station_wagon: station_wagon == 7, ("station_wagon",))

# 5. "The motorcyle is older than the truck" → motorcycle < truck
problem.addConstraint(lambda motorcycle, truck: motorcycle < truck, ("motorcycle", "truck"))

# 6. "The minivan is newer than the sedan" → minivan > sedan (i.e., minivan > 5)
problem.addConstraint(lambda minivan, sedan: minivan > sedan, ("minivan", "sedan"))

# 7. "The tractor is the third-oldest" → tractor == 3
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

# Find which vehicle is fourth-newest (rank = 4)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)
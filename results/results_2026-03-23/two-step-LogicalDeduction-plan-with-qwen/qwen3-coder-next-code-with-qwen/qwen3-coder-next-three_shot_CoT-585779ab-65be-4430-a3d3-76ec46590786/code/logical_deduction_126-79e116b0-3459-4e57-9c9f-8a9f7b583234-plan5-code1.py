from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["bus", "motorcycle", "hatchback", "station_wagon", "minivan", "truck", "limousine"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The station wagon is the fourth-newest" → position 4 (since 1=oldest, 7=newest)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# 2. "The motorcycle is newer than the truck" → motorcycle < truck
problem.addConstraint(lambda motorcycle, truck: motorcycle < truck, ["motorcycle", "truck"])

# 3. "The station wagon is older than the hatchback" → station_wagon > hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon > hatchback, ["station_wagon", "hatchback"])

# 4. "The minivan is newer than the hatchback" → minivan < hatchback
problem.addConstraint(lambda minivan, hatchback: minivan < hatchback, ["minivan", "hatchback"])

# 5. "The bus is newer than the minivan" → bus < minivan
problem.addConstraint(lambda bus, minivan: bus < minivan, ["bus", "minivan"])

# 6. "The truck is newer than the limousine" → truck < limousine
problem.addConstraint(lambda truck, limousine: truck < limousine, ["truck", "limousine"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "bus",
    "B": "motorcycle",
    "C": "hatchback",
    "D": "station_wagon",
    "E": "minivan",
    "F": "truck",
    "G": "limousine"
}

# Find the vehicle that is second-newest (position 6)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 6:
            print(letter)
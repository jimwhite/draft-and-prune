from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["bus", "motorcycle", "hatchback", "station_wagon", "minivan", "truck", "limousine"]

# Define the domain: ranks 1 to 7, where 1 = oldest and 7 = newest
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is the fourth-newest" → rank = 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# 3. "The motorcycle is newer than the truck" → motorcycle < truck
problem.addConstraint(lambda motorcycle, truck: motorcycle < truck, ["motorcycle", "truck"])

# 4. "The station wagon is older than the hatchback" → station_wagon > hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon > hatchback, ["station_wagon", "hatchback"])

# 5. "The minivan is newer than the hatchback" → minivan < hatchback
problem.addConstraint(lambda minivan, hatchback: minivan < hatchback, ["minivan", "hatchback"])

# 6. "The bus is newer than the minivan" → bus < minivan
problem.addConstraint(lambda bus, minivan: bus < minivan, ["bus", "minivan"])

# 7. "The truck is newer than the limousine" → truck < limousine
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

# Find the vehicle with rank 6 (second-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 6:
            print(letter)
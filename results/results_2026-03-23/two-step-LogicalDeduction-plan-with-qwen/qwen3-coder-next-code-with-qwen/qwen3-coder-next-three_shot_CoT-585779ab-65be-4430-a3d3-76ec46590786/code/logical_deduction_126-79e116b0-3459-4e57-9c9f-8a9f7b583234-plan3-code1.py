from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["bus", "motorcycle", "hatchback", "station_wagon", "minivan", "truck", "limousine"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The station wagon is the fourth-newest" → rank 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ["station_wagon"])

# "The motorcycle is newer than the truck" → motorcycle rank < truck rank
problem.addConstraint(lambda motorcycle, truck: motorcycle < truck, ["motorcycle", "truck"])

# "The station wagon is older than the hatchback" → station_wagon rank < hatchback rank
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ["station_wagon", "hatchback"])

# "The minivan is newer than the hatchback" → minivan rank < hatchback rank
problem.addConstraint(lambda minivan, hatchback: minivan < hatchback, ["minivan", "hatchback"])

# "The bus is newer than the minivan" → bus rank < minivan rank
problem.addConstraint(lambda bus, minivan: bus < minivan, ["bus", "minivan"])

# "The truck is newer than the limousine" → truck rank < limousine rank
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
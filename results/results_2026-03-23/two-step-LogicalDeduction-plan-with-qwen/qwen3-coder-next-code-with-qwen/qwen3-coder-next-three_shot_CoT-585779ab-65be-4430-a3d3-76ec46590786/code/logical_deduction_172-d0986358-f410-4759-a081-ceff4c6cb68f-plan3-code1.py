from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["limousine", "convertible", "station_wagon", "minivan", "bus", "tractor", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint to ensure unique positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The minivan is the oldest" → minivan == 1
problem.addConstraint(lambda minivan: minivan == 1, ["minivan"])

# 2. "The truck is older than the station wagon" → truck < station_wagon
problem.addConstraint(lambda truck, station_wagon: truck < station_wagon, ["truck", "station_wagon"])

# 3. "The truck is newer than the limousine" → limousine < truck
problem.addConstraint(lambda limousine, truck: limousine < truck, ["limousine", "truck"])

# 4. "The bus is newer than the convertible" → convertible < bus
problem.addConstraint(lambda convertible, bus: convertible < bus, ["convertible", "bus"])

# 5. "The bus is older than the tractor" → bus < tractor
problem.addConstraint(lambda bus, tractor: bus < tractor, ["bus", "tractor"])

# 6. "The limousine is newer than the tractor" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ["tractor", "limousine"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "limousine",
    "B": "convertible",
    "C": "station_wagon",
    "D": "minivan",
    "E": "bus",
    "F": "tractor",
    "G": "truck"
}

# Find the vehicle with rank 5 (third-newest: positions are 1=oldest, 7=newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
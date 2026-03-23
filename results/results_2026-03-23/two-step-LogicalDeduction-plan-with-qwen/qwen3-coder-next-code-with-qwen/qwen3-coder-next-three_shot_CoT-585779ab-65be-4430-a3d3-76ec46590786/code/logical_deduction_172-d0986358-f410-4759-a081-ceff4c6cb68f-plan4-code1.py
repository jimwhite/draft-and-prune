from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["limousine", "convertible", "station_wagon", "minivan", "bus", "tractor", "truck"]

# Define the domain: ranks 1 to 7, where 1 = oldest, 7 = newest
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraint that all vehicles have different ranks
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# 1. "The minivan is the oldest" → rank = 1
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

# Find the vehicle with rank 5 (third-newest: positions from newest are 7,6,5 → third-newest is rank 5)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)
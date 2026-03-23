from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (the seven vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["station_wagon", "truck", "sedan", "limousine", "convertible", "bus", "hatchback"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem description
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The limousine is the newest" → rank 7
problem.addConstraint(lambda limousine: limousine == 7, ["limousine"])

# 3. "The bus is the third-newest" → rank 5 (7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda bus: bus == 5, ["bus"])

# 4. "The bus is older than the convertible" → bus < convertible
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# 5. "The sedan is the third-oldest" → rank 3
problem.addConstraint(lambda sedan: sedan == 3, ["sedan"])

# 6. "The station wagon is older than the truck" → station_wagon < truck
problem.addConstraint(lambda station_wagon, truck: station_wagon < truck, ["station_wagon", "truck"])

# 7. "The hatchback is the oldest" → rank 1
problem.addConstraint(lambda hatchback: hatchback == 1, ["hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': "station_wagon",
    'B': "truck",
    'C': "sedan",
    'D': "limousine",
    'E': "convertible",
    'F': "bus",
    'G': "hatchback"
}

# Find which vehicle has rank 3 (third-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
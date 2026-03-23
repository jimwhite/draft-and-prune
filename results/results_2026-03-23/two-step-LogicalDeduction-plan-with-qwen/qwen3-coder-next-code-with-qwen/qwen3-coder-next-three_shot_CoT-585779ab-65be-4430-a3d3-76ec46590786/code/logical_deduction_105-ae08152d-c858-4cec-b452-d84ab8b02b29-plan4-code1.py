from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (positions 1 to 7, where 1=oldest, 7=newest)
vehicles = ["station_wagon", "truck", "sedan", "limousine", "convertible", "bus", "hatchback"]
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "The limousine is the newest" → position = 7
problem.addConstraint(lambda limousine: limousine == 7, ["limousine"])

# "The bus is the third-newest" → position = 5 (7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda bus: bus == 5, ["bus"])

# "The bus is older than the convertible" → bus < convertible
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# "The sedan is the third-oldest" → position = 3 (1=oldest, 2=second-oldest, 3=third-oldest)
problem.addConstraint(lambda sedan: sedan == 3, ["sedan"])

# "The station wagon is older than the truck" → station_wagon < truck
problem.addConstraint(lambda station_wagon, truck: station_wagon < truck, ["station_wagon", "truck"])

# "The hatchback is the oldest" → position = 1
problem.addConstraint(lambda hatchback: hatchback == 1, ["hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names as per the options
choices = {
    'A': "station_wagon",
    'B': "truck",
    'C': "sedan",
    'D': "limousine",
    'E': "convertible",
    'F': "bus",
    'G': "hatchback"
}

# Find which vehicle has position 3 (third-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
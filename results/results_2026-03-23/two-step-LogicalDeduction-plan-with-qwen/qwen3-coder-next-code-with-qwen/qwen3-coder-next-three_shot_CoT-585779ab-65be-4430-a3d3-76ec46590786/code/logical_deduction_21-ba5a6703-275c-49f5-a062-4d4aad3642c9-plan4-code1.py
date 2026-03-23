from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["truck", "motorcyle", "limousine", "station_wagon", "sedan"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is the oldest."
problem.addConstraint(lambda station_wagon: station_wagon == 1, ["station_wagon"])

# "The limousine is older than the truck."
problem.addConstraint(lambda limousine, truck: limousine < truck, ["limousine", "truck"])

# "The limousine is newer than the sedan."
problem.addConstraint(lambda sedan, limousine: sedan < limousine, ["sedan", "limousine"])

# "The sedan is newer than the motorcyle."
problem.addConstraint(lambda motorcyle, sedan: motorcyle < sedan, ["motorcyle", "sedan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "truck",
    "B": "motorcyle",
    "C": "limousine",
    "D": "station_wagon",
    "E": "sedan"
}

# Find the vehicle that is second-oldest (rank 2)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
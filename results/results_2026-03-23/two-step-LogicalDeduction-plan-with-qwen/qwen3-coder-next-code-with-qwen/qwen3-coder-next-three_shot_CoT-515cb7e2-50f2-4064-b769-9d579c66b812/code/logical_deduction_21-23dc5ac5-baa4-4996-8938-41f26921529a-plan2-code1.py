from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["truck", "motorcyle", "limousine", "station_wagon", "sedan"]
positions = range(1, 6)
problem.addVariables(vehicles, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The limousine is older than the truck" -> limousine < truck
problem.addConstraint(lambda limousine, truck: limousine < truck, ("limousine", "truck"))

# "The sedan is newer than the motorcyle" -> motorcyle < sedan
problem.addConstraint(lambda motorcyle, sedan: motorcyle < sedan, ("motorcyle", "sedan"))

# "The station wagon is the oldest" -> station_wagon == 1
problem.addConstraint(lambda station_wagon: station_wagon == 1, ("station_wagon",))

# "The limousine is newer than the sedan" -> sedan < limousine
problem.addConstraint(lambda sedan, limousine: sedan < limousine, ("sedan", "limousine"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "truck",
    "B": "motorcyle",
    "C": "limousine",
    "D": "station_wagon",
    "E": "sedan"
}

# Find the vehicle with position 2 (second-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
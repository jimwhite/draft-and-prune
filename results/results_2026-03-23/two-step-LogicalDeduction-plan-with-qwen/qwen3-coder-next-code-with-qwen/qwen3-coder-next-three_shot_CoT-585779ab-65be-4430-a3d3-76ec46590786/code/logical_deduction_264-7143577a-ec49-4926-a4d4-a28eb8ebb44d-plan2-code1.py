from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is older than the hatchback" -> station_wagon < hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# "The hatchback is the second-newest" -> hatchback == 2
problem.addConstraint(lambda hatchback: hatchback == 2, ("hatchback",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicles
choices = {
    "A": "hatchback",
    "B": "limousine",
    "C": "station_wagon"
}

# Find which vehicle is the newest (rank 3)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
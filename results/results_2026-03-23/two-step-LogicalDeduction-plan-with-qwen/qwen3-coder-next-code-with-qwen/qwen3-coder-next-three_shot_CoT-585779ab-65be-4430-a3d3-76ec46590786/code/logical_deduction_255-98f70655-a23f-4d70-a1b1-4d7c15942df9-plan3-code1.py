from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is older than the hatchback"
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# "The hatchback is the second-newest"
problem.addConstraint(lambda hatchback: hatchback == 2, ("hatchback",))

# Solve the problem
solutions = problem.getSolutions()

# Determine the correct answer
choices = {
    "A": "hatchback",
    "B": "limousine",
    "C": "station_wagon"
}

# Find the vehicle with rank 1 (oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 1:
            print(letter)
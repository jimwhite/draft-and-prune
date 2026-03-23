from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["bus", "sedan", "truck"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The truck is older than the bus" -> truck < bus
problem.addConstraint(lambda truck, bus: truck < bus, ("truck", "bus"))

# "The bus is older than the sedan" -> bus < sedan
problem.addConstraint(lambda bus, sedan: bus < sedan, ("bus", "sedan"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicles
choices = {
    "A": "bus",
    "B": "sedan",
    "C": "truck"
}

# Find the vehicle with rank 3 (newest) and print corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
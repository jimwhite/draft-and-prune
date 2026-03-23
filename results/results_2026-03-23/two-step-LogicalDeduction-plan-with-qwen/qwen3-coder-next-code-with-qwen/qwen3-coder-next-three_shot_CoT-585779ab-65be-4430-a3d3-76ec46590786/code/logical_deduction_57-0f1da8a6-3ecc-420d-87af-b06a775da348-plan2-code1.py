from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "sedan", "bus", "tractor"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the hatchback" → hatchback < tractor
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ("hatchback", "tractor"))

# "The bus is the second-oldest" → bus == 2
problem.addConstraint(lambda bus: bus == 2, ("bus",))

# "The hatchback is newer than the sedan" → sedan < hatchback
problem.addConstraint(lambda sedan, hatchback: sedan < hatchback, ("sedan", "hatchback"))

# "The limousine is the newest" → limousine == 5
problem.addConstraint(lambda limousine: limousine == 5, ("limousine",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "hatchback",
    "B": "limousine",
    "C": "sedan",
    "D": "bus",
    "E": "tractor"
}

# Find which vehicle is third-newest (rank 3)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
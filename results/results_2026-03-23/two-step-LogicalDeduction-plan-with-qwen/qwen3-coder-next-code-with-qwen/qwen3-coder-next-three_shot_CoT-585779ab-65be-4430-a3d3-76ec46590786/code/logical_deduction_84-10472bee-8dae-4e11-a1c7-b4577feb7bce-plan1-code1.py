from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the sedan"
problem.addConstraint(lambda minivan, sedan: minivan < sedan, ("minivan", "sedan"))

# "The tractor is older than the hatchback"
problem.addConstraint(lambda tractor, hatchback: tractor < hatchback, ("tractor", "hatchback"))

# "The minivan is the third-newest" -> position 3
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# "The station wagon is the second-newest" -> position 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the third-newest (position 3)
# According to constraints, minivan must be at position 3
# So choice C ("The minivan is the third-newest.") must be true

# Map choices to vehicles
choices = {
    "A": "tractor",
    "B": "station_wagon", 
    "C": "minivan",
    "D": "sedan",
    "E": "hatchback"
}

# Find which vehicle is at position 3 (third-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
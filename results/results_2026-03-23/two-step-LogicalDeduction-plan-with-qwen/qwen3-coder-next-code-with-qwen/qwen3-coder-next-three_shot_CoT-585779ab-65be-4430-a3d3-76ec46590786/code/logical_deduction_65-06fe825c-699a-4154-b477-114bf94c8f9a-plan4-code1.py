from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the sedan" → minivan < sedan
problem.addConstraint(lambda minivan, sedan: minivan < sedan, ("minivan", "sedan"))

# "The tractor is older than the hatchback" → tractor < hatchback
problem.addConstraint(lambda tractor, hatchback: tractor < hatchback, ("tractor", "hatchback"))

# "The minivan is the third-newest" → minivan == 3
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# "The station wagon is the second-newest" → station_wagon == 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Check which vehicle has rank 4 (second-newest)
for solution in solutions:
    for letter, statement in [
        ("A", "tractor"),
        ("B", "station_wagon"),
        ("C", "minivan"),
        ("D", "sedan"),
        ("E", "hatchback")
    ]:
        if solution[statement] == 4:
            print(letter)
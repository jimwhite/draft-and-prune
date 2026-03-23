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

# "The minivan is the third-newest" (position 3)
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# "The station wagon is the second-newest" (position 4)
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Check which vehicle is second-newest (rank 4)
for solution in solutions:
    if solution["tractor"] == 4:
        print("A")
    elif solution["station_wagon"] == 4:
        print("B")
    elif solution["minivan"] == 4:
        print("C")
    elif solution["sedan"] == 4:
        print("D")
    elif solution["hatchback"] == 4:
        print("E")
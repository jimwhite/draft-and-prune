from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the sedan" -> minivan < sedan
problem.addConstraint(lambda minivan, sedan: minivan < sedan, ("minivan", "sedan"))

# "The tractor is older than the hatchback" -> tractor < hatchback
problem.addConstraint(lambda tractor, hatchback: tractor < hatchback, ("tractor", "hatchback"))

# "The minivan is the third-newest" -> rank = 3 (since 5=newest, 4=second-newest, 3=third-newest)
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# "The station wagon is the second-newest" -> rank = 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# Check which vehicle is third-newest (rank 3) and match with choices
for solution in solutions:
    if solution["tractor"] == 3:
        print("A")
    elif solution["station_wagon"] == 3:
        print("B")
    elif solution["minivan"] == 3:
        print("C")
    elif solution["sedan"] == 3:
        print("D")
    elif solution["hatchback"] == 3:
        print("E")
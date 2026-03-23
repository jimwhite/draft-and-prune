from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks: 1=oldest, 5=newest)
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The minivan is older than the sedan" → minivan < sedan
problem.addConstraint(lambda minivan, sedan: minivan < sedan, ("minivan", "sedan"))

# "The tractor is older than the hatchback" → tractor < hatchback
problem.addConstraint(lambda tractor, hatchback: tractor < hatchback, ("tractor", "hatchback"))

# "The minivan is the third-newest" → rank = 3 (since 5=newest, 4=second-newest, 3=third-newest)
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# "The station wagon is the second-newest" → rank = 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the second-newest (rank 4)
# Check the solution to find which vehicle has rank 4
for solution in solutions:
    # The choices are labeled A through E, and we need to match the vehicle at rank 4
    # According to the choices:
    # A) The tractor is the second-newest.
    # B) The station wagon is the second-newest.
    # C) The minivan is the second-newest.
    # D) The sedan is the second-newest.
    # E) The hatchback is the second-newest.
    
    # From constraint: station_wagon == 4, so it's the second-newest
    if solution["station_wagon"] == 4:
        print("B")
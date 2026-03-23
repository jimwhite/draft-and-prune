from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["tractor", "station_wagon", "minivan", "sedan", "hatchback"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have distinct ranks
problem.addConstraint(AllDifferentConstraint())

# The minivan is older than the sedan: minivan < sedan
problem.addConstraint(lambda minivan, sedan: minivan < sedan, ("minivan", "sedan"))

# The tractor is older than the hatchback: tractor < hatchback
problem.addConstraint(lambda tractor, hatchback: tractor < hatchback, ("tractor", "hatchback"))

# The minivan is the third-newest: rank = 3
problem.addConstraint(lambda minivan: minivan == 3, ("minivan",))

# The station wagon is the second-newest: rank = 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve for the arrangement
solutions = problem.getSolutions()

# Find which vehicle has rank 4 (second-newest)
for solution in solutions:
    for vehicle, rank in solution.items():
        if rank == 4:
            # Map the vehicle to the corresponding choice letter
            if vehicle == "station_wagon":
                print("B")
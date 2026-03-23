from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is older than the hatchback"
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# "The hatchback is the second-newest" (rank 2)
problem.addConstraint(lambda hatchback: hatchback == 2, ["hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# Determine which vehicle is oldest (rank 1)
for solution in solutions:
    if solution["hatchback"] == 2:
        # Find which vehicle has rank 1
        if solution["limousine"] == 1:
            print("B")
        elif solution["station_wagon"] == 1:
            print("C")
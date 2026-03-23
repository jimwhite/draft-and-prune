from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)  # 1=oldest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The station wagon is older than the hatchback" -> station_wagon < hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# "The hatchback is the second-newest" -> hatchback == 2 (since newest=3, second-newest=2)
problem.addConstraint(lambda hatchback: hatchback == 2, ("hatchback",))

# Solve the problem
solutions = problem.getSolutions()

# Determine which vehicle is the newest (rank 3)
for solution in solutions:
    if solution["hatchback"] == 3:
        print("A")
    elif solution["limousine"] == 3:
        print("B")
    elif solution["station_wagon"] == 3:
        print("C")
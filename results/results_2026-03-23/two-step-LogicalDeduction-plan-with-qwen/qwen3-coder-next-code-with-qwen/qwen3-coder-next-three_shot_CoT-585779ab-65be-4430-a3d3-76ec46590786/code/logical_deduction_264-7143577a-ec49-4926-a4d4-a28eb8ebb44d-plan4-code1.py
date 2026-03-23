from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)  # 1=oldest, 2=middle, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is older than the hatchback" -> station_wagon < hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# 3. "The hatchback is the second-newest" -> hatchback == 2
problem.addConstraint(lambda hatchback: hatchback == 2, ("hatchback",))

# Solve the problem
solutions = problem.getSolutions()

# Find which vehicle is the newest (rank 3)
for solution in solutions:
    if solution["hatchback"] == 2:
        # hatchback is second-newest (rank 2), so newest must be either limousine or station_wagon
        # But station_wagon is older than hatchback (rank < 2), so station_wagon must be rank 1
        # Therefore limousine must be rank 3 (newest)
        if solution["station_wagon"] == 1:
            print("B")
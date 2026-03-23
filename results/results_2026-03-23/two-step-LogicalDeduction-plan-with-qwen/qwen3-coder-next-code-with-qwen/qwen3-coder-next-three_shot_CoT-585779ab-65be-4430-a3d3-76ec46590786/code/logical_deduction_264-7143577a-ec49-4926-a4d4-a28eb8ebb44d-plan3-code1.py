from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (three vehicles) and domain (age ranks 1 to 3)
vehicles = ["hatchback", "limousine", "station_wagon"]
ranks = range(1, 4)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The station wagon is older than the hatchback" (smaller rank number)
problem.addConstraint(lambda station_wagon, hatchback: station_wagon < hatchback, ("station_wagon", "hatchback"))

# 3. "The hatchback is the second-newest" (rank 2 in our system where 1=oldest, 3=newest)
problem.addConstraint(lambda hatchback: hatchback == 2, ("hatchback",))

# Solve for the arrangement
solutions = problem.getSolutions()

# Determine which vehicle is the newest (rank 3)
for solution in solutions:
    # Find the vehicle with rank 3
    for vehicle, rank in solution.items():
        if rank == 3:
            # Map to choice letters: A=hatchback, B=limousine, C=station_wagon
            if vehicle == "hatchback":
                print("A")
            elif vehicle == "limousine":
                print("B")
            elif vehicle == "station_wagon":
                print("C")
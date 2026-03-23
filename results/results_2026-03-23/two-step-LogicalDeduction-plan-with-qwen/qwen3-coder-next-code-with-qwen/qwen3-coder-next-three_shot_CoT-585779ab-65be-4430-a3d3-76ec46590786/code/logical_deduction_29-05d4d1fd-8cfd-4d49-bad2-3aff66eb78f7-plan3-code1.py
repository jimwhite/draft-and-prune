from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["truck", "station_wagon", "motorcycle", "convertible", "hatchback"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The convertible is newer than the truck" → convertible > truck
problem.addConstraint(lambda convertible, truck: convertible > truck, ("convertible", "truck"))

# "The station wagon is newer than the hatchback" → station_wagon > hatchback
problem.addConstraint(lambda station_wagon, hatchback: station_wagon > hatchback, ("station_wagon", "hatchback"))

# "The convertible is older than the hatchback" → convertible < hatchback
problem.addConstraint(lambda convertible, hatchback: convertible < hatchback, ("convertible", "hatchback"))

# "The station wagon is the second-newest" → station_wagon == 4
problem.addConstraint(lambda station_wagon: station_wagon == 4, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the second-newest (rank 4)
# According to the constraint, station_wagon must be 4
# So choice B is correct: "The station wagon is the second-newest."
print("B")
from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["hatchback", "convertible", "tractor", "truck", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is newer than the hatchback" → tractor > hatchback
problem.addConstraint(lambda hatchback, tractor: hatchback < tractor, ["hatchback", "tractor"])

# 3. "The limousine is the second-newest" → limousine == 4
problem.addConstraint(lambda limousine: limousine == 4, ["limousine"])

# 4. "The truck is older than the hatchback" → truck < hatchback
problem.addConstraint(lambda truck, hatchback: truck < hatchback, ["truck", "hatchback"])

# 5. "The convertible is the second-oldest" → convertible == 2
problem.addConstraint(lambda convertible: convertible == 2, ["convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Map vehicles to choice letters for the question about second-newest (rank 4)
vehicle_to_choice = {
    "hatchback": "A",
    "convertible": "B",
    "tractor": "C",
    "truck": "D",
    "limousine": "E"
}

# Find which vehicle has rank 4 (second-newest) and print its choice letter
for solution in solutions:
    for vehicle, rank in solution.items():
        if rank == 4:
            print(vehicle_to_choice[vehicle])
from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 2=second-newest/middle, 3=newest)
vehicles = ["sedan", "minivan", "motorcycle"]
ranks = [1, 2, 3]
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The motorcycle is the second-newest" → rank = 2
problem.addConstraint(lambda motorcycle: motorcycle == 2, ["motorcycle"])

# 3. "The minivan is newer than the motorcycle" → minivan > 2, so minivan == 3
problem.addConstraint(lambda minivan: minivan > 2, ["minivan"])

# Solve the problem
solutions = problem.getSolutions()

# Since there's only one solution, get it directly
solution = solutions[0]

# Check which vehicle is second-newest (rank 2) and match with choices
if solution["sedan"] == 2:
    print("A")
elif solution["minivan"] == 2:
    print("B")
elif solution["motorcycle"] == 2:
    print("C")
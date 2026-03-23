from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["bus", "truck", "motorcycle", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The sedan is the second-oldest" → rank = 2
problem.addConstraint(lambda sedan: sedan == 2, ["sedan"])

# 3. "The hatchback is newer than the motorcycle" → hatchback > motorcycle
problem.addConstraint(lambda hatchback, motorcycle: hatchback > motorcycle, ["hatchback", "motorcycle"])

# 4. "The motorcycle is newer than the sedan" → motorcycle > sedan
problem.addConstraint(lambda motorcycle, sedan: motorcycle > sedan, ["motorcycle", "sedan"])

# 5. "The hatchback is older than the truck" → hatchback < truck
problem.addConstraint(lambda hatchback, truck: hatchback < truck, ["hatchback", "truck"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the second-oldest (rank 2)
# Check each solution to find which vehicle has rank 2
for solution in solutions:
    if solution["sedan"] == 2:
        print("D")
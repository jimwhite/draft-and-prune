from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["station_wagon", "sedan", "tractor", "motorcycle", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The tractor is newer than the motorcycle" → tractor > motorcycle
problem.addConstraint(lambda tractor, motorcycle: tractor > motorcycle, ("tractor", "motorcycle"))

# 3. "The motorcycle is newer than the sedan" → motorcycle > sedan
problem.addConstraint(lambda motorcycle, sedan: motorcycle > sedan, ("motorcycle", "sedan"))

# 4. "The limousine is the oldest" → limousine == 1
problem.addConstraint(lambda limousine: limousine == 1, ("limousine",))

# 5. "The station wagon is the newest" → station_wagon == 5
problem.addConstraint(lambda station_wagon: station_wagon == 5, ("station_wagon",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the oldest (rank 1)
# According to constraint #4, limousine must be rank 1
# So choice E is correct: "The limousine is the oldest."
print("E")
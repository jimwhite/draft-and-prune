from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the five vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "sedan", "station_wagon", "bus", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The sedan is newer than the station wagon" → sedan > station_wagon
problem.addConstraint(lambda sedan, station_wagon: sedan > station_wagon, ("sedan", "station_wagon"))

# 3. "The limousine is the newest" → limousine == 5
problem.addConstraint(lambda limousine: limousine == 5, ("limousine",))

# 4. "The bus is the second-newest" → bus == 4
problem.addConstraint(lambda bus: bus == 4, ("bus",))

# 5. "The convertible is the second-oldest" → convertible == 2
problem.addConstraint(lambda convertible: convertible == 2, ("convertible",))

# Solve for the unique arrangement
solutions = problem.getSolutions()

# Since there's only one solution, get it directly
solution = solutions[0]

# The question asks which statement is true, and choice A states "The convertible is the second-oldest."
# We verify this by checking if convertible's rank is 2
if solution["convertible"] == 2:
    print("A")
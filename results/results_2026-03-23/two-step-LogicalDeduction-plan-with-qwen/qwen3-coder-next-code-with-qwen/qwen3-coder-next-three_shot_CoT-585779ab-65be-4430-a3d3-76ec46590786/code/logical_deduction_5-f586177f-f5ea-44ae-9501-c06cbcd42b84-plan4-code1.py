from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "sedan", "station_wagon", "bus", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# The sedan is newer than the station wagon (sedan rank > station_wagon rank)
problem.addConstraint(lambda s, sw: s > sw, ("sedan", "station_wagon"))

# The limousine is the newest (rank = 5)
problem.addConstraint(lambda l: l == 5, ("limousine",))

# The bus is the second-newest (rank = 4)
problem.addConstraint(lambda b: b == 4, ("bus",))

# The convertible is the second-oldest (rank = 2)
problem.addConstraint(lambda c: c == 2, ("convertible",))

# Solve the problem
solutions = problem.getSolutions()

# Since we have a unique solution, take the first one
solution = solutions[0]

# The question asks which statement is true. Choice A directly states that
# "The convertible is the second-oldest", which matches our constraint.
# We verify that in the solution, convertible has rank 2 (which it must by constraint)
if solution["convertible"] == 2:
    print("A")
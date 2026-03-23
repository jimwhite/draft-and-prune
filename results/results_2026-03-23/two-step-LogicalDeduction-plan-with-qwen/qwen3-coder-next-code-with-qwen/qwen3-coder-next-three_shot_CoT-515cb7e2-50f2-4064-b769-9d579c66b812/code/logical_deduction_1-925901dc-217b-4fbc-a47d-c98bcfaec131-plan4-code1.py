from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "sedan", "tractor", "minivan", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
# All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the minivan" → tractor > minivan
problem.addConstraint(lambda tractor, minivan: tractor > minivan, ("tractor", "minivan"))

# "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The convertible is older than the sedan" → convertible < sedan
problem.addConstraint(lambda convertible, sedan: convertible < sedan, ("convertible", "sedan"))

# "The convertible is the second-newest" → convertible == 4
problem.addConstraint(lambda convertible: convertible == 4, ("convertible",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which statement is true, and choice A directly states the given fact
# Since convertible == 4 is explicitly enforced as a constraint, and it matches choice A,
# we verify this in the solution and output 'A'
for solution in solutions:
    if solution["convertible"] == 4:
        print("A")
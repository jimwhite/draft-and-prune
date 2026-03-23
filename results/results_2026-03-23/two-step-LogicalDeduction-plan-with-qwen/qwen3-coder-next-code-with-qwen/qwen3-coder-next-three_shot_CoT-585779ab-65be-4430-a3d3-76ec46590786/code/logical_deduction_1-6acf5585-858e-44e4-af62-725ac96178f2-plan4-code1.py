from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "sedan", "tractor", "minivan", "limousine"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The tractor is newer than the minivan" -> tractor > minivan
problem.addConstraint(lambda tractor, minivan: tractor > minivan, ("tractor", "minivan"))

# "The tractor is older than the limousine" -> tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The convertible is older than the sedan" -> convertible < sedan
problem.addConstraint(lambda convertible, sedan: convertible < sedan, ("convertible", "sedan"))

# "The convertible is the second-newest" -> convertible == 4
problem.addConstraint(lambda convertible: convertible == 4, ("convertible",))

# Solve the problem
solutions = problem.getSolutions()

# Since the problem is consistent and has a unique solution, we can check the first (and only) solution
solution = solutions[0]

# The question asks which statement is true, and choice A directly states "The convertible is the second-newest"
# We know from our constraint that convertible == 4, which means it is the second-newest
# So choice A must be true

print("A")
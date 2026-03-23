from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "sedan", "tractor", "minivan", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
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

# Map choice letters to vehicles
choices = {
    'A': 'convertible',
    'B': 'sedan',
    'C': 'tractor',
    'D': 'minivan',
    'E': 'limousine'
}

# Find the vehicle that is third-newest (rank 3)
for solution in solutions:
    for letter, vehicle in choices.items():
        if solution[vehicle] == 3:
            print(letter)
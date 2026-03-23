from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["minivan", "bus", "limousine", "truck", "convertible", "tractor", "motorcycle"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "The limousine is older than the minivan" → limousine < minivan
problem.addConstraint(lambda limousine, minivan: limousine < minivan, ("limousine", "minivan"))

# "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# "The bus is the newest" → bus == 7
problem.addConstraint(lambda bus: bus == 7, ("bus",))

# "The truck is the third-newest" → truck == 5 (since newest=7, second-newest=6, third-newest=5)
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# "The motorcycle is the fourth-newest" → motorcycle == 4 (7-3=4)
problem.addConstraint(lambda motorcycle: motorcycle == 4, ("motorcycle",))

# "The convertible is older than the tractor" → convertible < tractor
problem.addConstraint(lambda convertible, tractor: convertible < tractor, ("convertible", "tractor"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': "minivan",
    'B': "bus",
    'C': "limousine",
    'D': "truck",
    'E': "convertible",
    'F': "tractor",
    'G': "motorcycle"
}

# Find which vehicle has rank 3 (third-oldest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)
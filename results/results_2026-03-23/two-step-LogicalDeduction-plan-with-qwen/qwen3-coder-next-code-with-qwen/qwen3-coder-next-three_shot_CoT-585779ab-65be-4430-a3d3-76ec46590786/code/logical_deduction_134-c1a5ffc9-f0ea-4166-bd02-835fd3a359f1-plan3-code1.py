from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven vehicles as variables
vehicles = ["limousine", "truck", "sedan", "tractor", "minivan", "motorcycle", "hatchback"]

# Define the domain: positions 1 to 7, where 1 = oldest and 7 = newest
positions = range(1, 8)
problem.addVariables(vehicles, positions)

# Add constraints based on the problem statements
# 1. All vehicles must have unique positions
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is older than the tractor" → minivan < tractor
problem.addConstraint(lambda minivan, tractor: minivan < tractor, ("minivan", "tractor"))

# 3. "The hatchback is older than the sedan" → hatchback < sedan
problem.addConstraint(lambda hatchback, sedan: hatchback < sedan, ("hatchback", "sedan"))

# 4. "The truck is the third-newest" → position = 5 (since newest=7, second-newest=6, third-newest=5)
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# 5. "The hatchback is the second-newest" → position = 6
problem.addConstraint(lambda hatchback: hatchback == 6, ("hatchback",))

# 6. "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# 7. "The motorcycle is newer than the limousine" → limousine < motorcycle
problem.addConstraint(lambda limousine, motorcycle: limousine < motorcycle, ("limousine", "motorcycle"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    "A": "limousine",
    "B": "truck",
    "C": "sedan",
    "D": "tractor",
    "E": "minivan",
    "F": "motorcycle",
    "G": "hatchback"
}

# Find the vehicle with position 2 (second-oldest) and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)
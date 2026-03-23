from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the variables (the seven vehicles) and their domain (age ranks 1 to 7)
# 1 = oldest, 7 = newest
vehicles = ["limousine", "sedan", "tractor", "motorcycle", "minivan", "hatchback", "truck"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle's statements
# 1. All vehicles must have a different age rank.
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is newer than the limousine" → minivan > limousine
problem.addConstraint(lambda minivan, limousine: minivan > limousine, ("minivan", "limousine"))

# 3. "The tractor is the second-newest" → rank = 6
problem.addConstraint(lambda tractor: tractor == 6, ("tractor",))

# 4. "The truck is older than the sedan" → truck < sedan
problem.addConstraint(lambda truck, sedan: truck < sedan, ("truck", "sedan"))

# 5. "The minivan is older than the truck" → minivan < truck
problem.addConstraint(lambda minivan, truck: minivan < truck, ("minivan", "truck"))

# 6. "The hatchback is newer than the tractor" → hatchback > tractor
problem.addConstraint(lambda hatchback, tractor: hatchback > tractor, ("hatchback", "tractor"))

# 7. "The motorcyle is the fourth-newest" → rank = 4
problem.addConstraint(lambda motorcycle: motorcycle == 4, ("motorcycle",))

# Find the solution(s)
solutions = problem.getSolutions()

# Map choice letters to vehicle names
choices = {
    'A': "limousine",
    'B': "sedan",
    'C': "tractor",
    'D': "motorcycle",
    'E': "minivan",
    'F': "hatchback",
    'G': "truck"
}

# Find which vehicle has rank 7 (newest) and print the corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 7:
            print(letter)
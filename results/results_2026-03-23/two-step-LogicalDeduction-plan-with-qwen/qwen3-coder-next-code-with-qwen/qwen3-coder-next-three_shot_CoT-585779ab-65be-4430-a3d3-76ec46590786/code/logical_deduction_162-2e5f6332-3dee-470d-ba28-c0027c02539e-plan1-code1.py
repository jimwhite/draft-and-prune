from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (the seven vehicles) and domain (age ranks 1 to 7, where 1=oldest, 7=newest)
vehicles = ["limousine", "truck", "sedan", "tractor", "minivan", "motorcyle", "hatchback"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add constraints based on the puzzle statements
# 1. All vehicles must have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The minivan is older than the tractor" → minivan < tractor
problem.addConstraint(lambda minivan, tractor: minivan < tractor, ("minivan", "tractor"))

# 3. "The hatchback is older than the sedan" → hatchback < sedan
problem.addConstraint(lambda hatchback, sedan: hatchback < sedan, ("hatchback", "sedan"))

# 4. "The truck is the third-newest" → rank = 5 (since newest=7, second-newest=6, third-newest=5)
problem.addConstraint(lambda truck: truck == 5, ("truck",))

# 5. "The hatchback is the second-newest" → rank = 6
problem.addConstraint(lambda hatchback: hatchback == 6, ("hatchback",))

# 6. "The tractor is older than the limousine" → tractor < limousine
problem.addConstraint(lambda tractor, limousine: tractor < limousine, ("tractor", "limousine"))

# 7. "The motorcyle is newer than the limousine" → limousine < motorcyle
problem.addConstraint(lambda limousine, motorcyle: limousine < motorcyle, ("limousine", "motorcyle"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names based on the choices list
choices_map = {
    "A": "limousine",
    "B": "truck",
    "C": "sedan",
    "D": "tractor",
    "E": "minivan",
    "F": "motorcyle",
    "G": "hatchback"
}

# Find the vehicle with rank 7 (newest) and print its corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices_map.items():
        if solution[vehicle_name] == 7:
            print(letter)
from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
golfers = ["amy", "ana", "joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Ana" → Amy's position > Ana's position
problem.addConstraint(lambda amy, ana: amy > ana, ["amy", "ana"])

# "Ana finished below Joe" → Ana's position > Joe's position
problem.addConstraint(lambda ana, joe: ana > joe, ["ana", "joe"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "amy",
    "B": "ana",
    "C": "joe"
}

# Find who finished first (position 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
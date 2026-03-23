from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["amy", "ana", "joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Ana" → Amy's position > Ana's position
problem.addConstraint(lambda amy, ana: amy > ana, ["amy", "ana"])

# "Ana finished below Joe" → Ana's position > Joe's position
problem.addConstraint(lambda ana, joe: ana > joe, ["ana", "joe"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "amy",
    "B": "ana",
    "C": "joe"
}

# Find the golfer who finished first (position 1)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 1:
            print(letter)
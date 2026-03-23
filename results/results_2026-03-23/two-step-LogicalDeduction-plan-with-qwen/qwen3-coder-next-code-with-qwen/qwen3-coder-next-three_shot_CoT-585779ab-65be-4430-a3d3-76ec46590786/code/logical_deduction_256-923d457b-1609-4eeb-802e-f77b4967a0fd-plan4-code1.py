from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["amy", "ana", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# 1. All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Amy finished below Ana" → Amy's position > Ana's position
problem.addConstraint(lambda amy, ana: amy > ana, ["amy", "ana"])

# 3. "Ana finished below Joe" → Ana's position > Joe's position
problem.addConstraint(lambda ana, joe: ana > joe, ["ana", "Joe"])

# Solve for the finishing order
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "amy",
    "B": "ana",
    "C": "Joe"
}

# Find which golfer finished first (position 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
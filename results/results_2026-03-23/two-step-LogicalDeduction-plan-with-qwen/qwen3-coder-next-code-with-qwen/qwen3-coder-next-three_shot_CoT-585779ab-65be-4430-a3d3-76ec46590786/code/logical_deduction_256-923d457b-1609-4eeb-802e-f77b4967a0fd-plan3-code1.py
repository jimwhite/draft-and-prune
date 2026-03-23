from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finish positions: 1=first, 2=second, 3=third)
golfers = ["amy", "ana", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finish positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Ana" means Amy's position number is greater than Ana's
problem.addConstraint(lambda amy, ana: amy > ana, ["amy", "ana"])

# "Ana finished below Joe" means Ana's position number is greater than Joe's
problem.addConstraint(lambda ana, Joe: ana > Joe, ["ana", "Joe"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "amy",
    "B": "ana",
    "C": "Joe"
}

# Find who finished first (position 1) and print the corresponding letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
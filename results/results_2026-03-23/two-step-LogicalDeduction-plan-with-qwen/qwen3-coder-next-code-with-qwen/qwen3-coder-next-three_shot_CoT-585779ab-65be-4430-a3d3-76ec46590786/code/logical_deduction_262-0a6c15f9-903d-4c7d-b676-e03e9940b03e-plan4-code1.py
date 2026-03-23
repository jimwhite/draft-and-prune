from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["Dan", "Mel", "Amy"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Dan finished above Amy" means Dan's position number is less than Amy's
problem.addConstraint(lambda Dan, Amy: Dan < Amy, ["Dan", "Amy"])

# "Amy finished above Mel" means Amy's position number is less than Mel's
problem.addConstraint(lambda Amy, Mel: Amy < Mel, ["Amy", "Mel"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Dan",
    "B": "Mel",
    "C": "Amy"
}

# Find who finished first (position 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
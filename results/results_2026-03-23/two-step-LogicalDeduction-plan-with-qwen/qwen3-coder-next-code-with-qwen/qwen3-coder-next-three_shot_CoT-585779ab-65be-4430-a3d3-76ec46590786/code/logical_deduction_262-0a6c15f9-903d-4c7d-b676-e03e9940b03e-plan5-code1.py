from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["Dan", "Mel", "Amy"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished above Amy: Dan's rank < Amy's rank
problem.addConstraint(lambda Dan, Amy: Dan < Amy, ["Dan", "Amy"])

# Amy finished above Mel: Amy's rank < Mel's rank
problem.addConstraint(lambda Amy, Mel: Amy < Mel, ["Amy", "Mel"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfer names
choices = {
    "A": "Dan",
    "B": "Mel",
    "C": "Amy"
}

# Find who finished first (rank = 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
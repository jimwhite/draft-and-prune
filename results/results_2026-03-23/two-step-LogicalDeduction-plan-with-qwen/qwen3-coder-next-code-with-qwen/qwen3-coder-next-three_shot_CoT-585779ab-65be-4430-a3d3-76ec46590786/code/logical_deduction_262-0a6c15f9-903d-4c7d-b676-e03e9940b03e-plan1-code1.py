from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Dan", "Mel", "Amy"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Dan finished above Amy: Dan's position < Amy's position
problem.addConstraint(lambda dan, amy: dan < amy, ["Dan", "Amy"])

# Amy finished above Mel: Amy's position < Mel's position
problem.addConstraint(lambda amy, mel: amy < mel, ["Amy", "Mel"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
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
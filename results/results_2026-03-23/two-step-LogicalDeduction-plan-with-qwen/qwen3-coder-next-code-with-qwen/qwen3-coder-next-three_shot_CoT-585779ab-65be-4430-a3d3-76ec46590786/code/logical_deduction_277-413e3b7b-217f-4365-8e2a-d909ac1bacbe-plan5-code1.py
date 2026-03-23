from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["eve", "amy", "rob"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Amy finished above Rob" means Amy's position number is less than Rob's
problem.addConstraint(lambda amy, rob: amy < rob, ["amy", "rob"])

# 3. "Eve finished above Amy" means Eve's position number is less than Amy's
problem.addConstraint(lambda eve, amy: eve < amy, ["eve", "amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "eve",
    "B": "amy",
    "C": "rob"
}

# Find who finished second (position = 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
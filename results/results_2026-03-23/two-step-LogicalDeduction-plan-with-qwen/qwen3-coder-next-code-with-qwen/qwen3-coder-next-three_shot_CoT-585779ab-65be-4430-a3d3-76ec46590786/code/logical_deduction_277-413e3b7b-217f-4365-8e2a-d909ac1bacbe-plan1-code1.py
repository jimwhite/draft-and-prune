from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Eve", "Amy", "Rob"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Amy finished above Rob: Amy's position < Rob's position
problem.addConstraint(lambda amy, rob: amy < rob, ["Amy", "Rob"])

# Eve finished above Amy: Eve's position < Amy's position
problem.addConstraint(lambda eve, amy: eve < amy, ["Eve", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Eve",
    "B": "Amy",
    "C": "Rob"
}

# Find who finished second (position 2)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 2:
            print(letter)
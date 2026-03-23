from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Joe finished above Ana" means Joe's position < Ana's position
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# "Rob finished second" means Rob's position == 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfer names
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find who finished first (position 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
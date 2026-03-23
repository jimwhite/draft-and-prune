from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (positions 1=first, 2=second, 3=third)
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# 1. All golfers must have unique positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Joe finished above Ana" means Joe's position number is less than Ana's
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# 3. "Rob finished second" means Rob's position is exactly 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find who finished first (position 1) and print the corresponding letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
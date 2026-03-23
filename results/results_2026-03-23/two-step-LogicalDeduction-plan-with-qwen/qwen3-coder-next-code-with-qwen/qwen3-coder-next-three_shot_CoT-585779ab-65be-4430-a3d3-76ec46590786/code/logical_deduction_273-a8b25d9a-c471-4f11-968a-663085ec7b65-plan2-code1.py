from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=third)
golfers = ["Ana", "Rob", "Joe"]
positions = [1, 2, 3]
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's rank is numerically smaller than Ana's)
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# Rob finished second
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find who finished first (position 1) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
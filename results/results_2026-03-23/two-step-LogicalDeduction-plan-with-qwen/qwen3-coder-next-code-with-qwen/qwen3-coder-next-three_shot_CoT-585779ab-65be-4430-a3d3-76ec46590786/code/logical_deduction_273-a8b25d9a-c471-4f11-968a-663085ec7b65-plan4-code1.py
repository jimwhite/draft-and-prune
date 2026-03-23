from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1=first, 2=second, 3=third)
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's position number is less than Ana's)
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# Rob finished second
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find which golfer finished first (position 1)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 1:
            print(letter)
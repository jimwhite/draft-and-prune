from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 3, where 1 = first/best, 3 = last/worst)
golfers = ["ana", "rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's position number < Ana's position number)
problem.addConstraint(lambda j, a: j < a, ["Joe", "ana"])

# Rob finished second (position = 2)
problem.addConstraint(lambda r: r == 2, ["rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "ana",
    "B": "rob",
    "C": "Joe"
}

# Find which golfer finished last (position 3) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 3, where 1 = first place)
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's position number < Ana's position number)
problem.addConstraint(lambda joe, ana: joe < ana, ["Joe", "Ana"])

# Rob finished second (position = 2)
problem.addConstraint(lambda rob: rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find which golfer finished last (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
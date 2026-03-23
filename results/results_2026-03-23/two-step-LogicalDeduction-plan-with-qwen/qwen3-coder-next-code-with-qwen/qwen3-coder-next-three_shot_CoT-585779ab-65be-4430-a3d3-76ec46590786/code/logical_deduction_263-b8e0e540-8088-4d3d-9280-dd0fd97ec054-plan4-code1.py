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
problem.addConstraint(lambda joe, ana: joe < ana, ["Joe", "Ana"])

# "Rob finished second" means Rob's position == 2
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
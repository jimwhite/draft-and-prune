from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana: Joe's position < Ana's position
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# Rob finished above Joe: Rob's position < Joe's position
problem.addConstraint(lambda Rob, Joe: Rob < Joe, ["Rob", "Joe"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find who finished second (position 2)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 2:
            print(letter)
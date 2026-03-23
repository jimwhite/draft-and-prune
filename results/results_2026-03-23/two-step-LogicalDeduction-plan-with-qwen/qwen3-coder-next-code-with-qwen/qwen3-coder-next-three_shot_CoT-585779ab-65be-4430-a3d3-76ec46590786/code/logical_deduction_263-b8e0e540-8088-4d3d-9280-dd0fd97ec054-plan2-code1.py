from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)  # 1=first (highest), 3=last
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Joe finished above Ana" means Joe's position number < Ana's position number
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# "Rob finished second" means Rob's position = 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find who finished last (position 3)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)
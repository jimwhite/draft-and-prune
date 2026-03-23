from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Ana", "Rob", "Joe"]
ranks = range(1, 4)
problem.addVariables(golfers, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Joe finished above Ana" means Joe's rank is less than Ana's
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# "Rob finished second" means Rob's rank is 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find the golfer with rank 1 (first place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
golfers = ["Amy", "Eli", "Eve"]
ranks = range(1, 4)  # 1 = first (highest), 3 = last (lowest)
problem.addVariables(golfers, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Eve finished above Amy" means Eve's rank < Amy's rank
problem.addConstraint(lambda eve, amy: eve < amy, ["Eve", "Amy"])

# "Eli finished below Amy" means Eli's rank > Amy's rank
problem.addConstraint(lambda eli, amy: eli > amy, ["Eli", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Amy",
    "B": "Eli",
    "C": "Eve"
}

# Find who finished last (rank 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
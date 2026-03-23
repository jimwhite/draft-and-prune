from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
golfers = ["Amy", "Dan", "Mel"]
ranks = range(1, 4)  # 1 = first place (highest rank), 3 = last place
problem.addVariables(golfers, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Mel finished above Amy" means Mel's rank < Amy's rank
problem.addConstraint(lambda mel, amy: mel < amy, ["Mel", "Amy"])

# "Dan finished below Amy" means Dan's rank > Amy's rank
problem.addConstraint(lambda dan, amy: dan > amy, ["Dan", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Amy",
    "B": "Dan",
    "C": "Mel"
}

# Find who finished last (rank = 3)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)
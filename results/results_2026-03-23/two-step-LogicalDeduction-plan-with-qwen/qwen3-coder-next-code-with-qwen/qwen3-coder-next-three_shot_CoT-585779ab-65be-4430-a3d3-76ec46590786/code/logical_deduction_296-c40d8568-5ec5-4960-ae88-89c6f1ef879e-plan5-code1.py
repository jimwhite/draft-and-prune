from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
golfers = ["amy", "dan", "mel"]
ranks = range(1, 4)  # 1 = first (highest), 3 = last (lowest)
problem.addVariables(golfers, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Mel finished above Amy" means Mel's rank < Amy's rank
problem.addConstraint(lambda mel, amy: mel < amy, ("mel", "amy"))

# "Dan finished below Amy" means Dan's rank > Amy's rank (i.e., amy < dan)
problem.addConstraint(lambda amy, dan: amy < dan, ("amy", "dan"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "amy",
    "B": "dan",
    "C": "mel"
}

# Find who finished last (rank 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
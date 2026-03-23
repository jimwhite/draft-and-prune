from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
golfers = ["amy", "dan", "mel"]
positions = range(1, 4)  # 1=first (highest), 3=last
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Mel finished above Amy" means Mel's position number is less than Amy's
problem.addConstraint(lambda mel, amy: mel < amy, ("mel", "amy"))

# "Dan finished below Amy" means Dan's position number is greater than Amy's
problem.addConstraint(lambda amy, dan: amy < dan, ("amy", "dan"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "amy",
    "B": "dan",
    "C": "mel"
}

# Find who finished last (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
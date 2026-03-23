from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 3, where 1 = first place)
golfers = ["amy", "dan", "mel"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finish positions
problem.addConstraint(AllDifferentConstraint())

# "Mel finished above Amy" means mel's position number is less than amy's
problem.addConstraint(lambda mel, amy: mel < amy, ("mel", "amy"))

# "Dan finished below Amy" means dan's position number is greater than amy's
problem.addConstraint(lambda dan, amy: dan > amy, ("dan", "amy"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "amy",
    "B": "dan",
    "C": "mel"
}

# Find who finished last (position 3)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)
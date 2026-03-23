from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 3, where 1 = first place)
golfers = ["eve", "amy", "rob"]
ranks = range(1, 4)
problem.addVariables(golfers, ranks)

# Add constraints based on the puzzle statements
# 1. All golfers must have different ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "Amy finished above Rob" means amy's rank < rob's rank
problem.addConstraint(lambda amy, rob: amy < rob, ("amy", "rob"))

# 3. "Eve finished above Amy" means eve's rank < amy's rank
problem.addConstraint(lambda eve, amy: eve < amy, ("eve", "amy"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names for the second place (rank 2)
choices = {
    "A": "eve",
    "B": "amy",
    "C": "rob"
}

# Find which golfer has rank 2 and print the corresponding letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
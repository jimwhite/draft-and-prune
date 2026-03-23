from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 3, where 1 = first place)
golfers = ["Ana", "Rob", "Joe"]
ranks = range(1, 4)
problem.addVariables(golfers, ranks)

# Add constraints based on the statements
# 1. All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "Joe finished above Ana" → Joe's rank is smaller than Ana's
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ("Joe", "Ana"))

# 3. "Rob finished above Joe" → Rob's rank is smaller than Joe's
problem.addConstraint(lambda Rob, Joe: Rob < Joe, ("Rob", "Joe"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find who finished second (rank == 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
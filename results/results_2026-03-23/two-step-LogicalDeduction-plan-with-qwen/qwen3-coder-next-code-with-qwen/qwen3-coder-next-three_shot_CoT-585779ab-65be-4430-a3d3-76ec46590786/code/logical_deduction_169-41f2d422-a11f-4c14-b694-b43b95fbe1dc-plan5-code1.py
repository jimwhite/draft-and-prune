from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = first place)
golfers = ["Joe", "Dan", "Ana", "Mel", "Ada", "Eve", "Amy"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Eve finished above Amy" → Eve's rank < Amy's rank
problem.addConstraint(lambda eve, amy: eve < amy, ["Eve", "Amy"])

# "Dan finished second" → Dan's rank == 2
problem.addConstraint(lambda dan: dan == 2, ["Dan"])

# "Ada finished below Ana" → Ana's rank < Ada's rank
problem.addConstraint(lambda ana, ada: ana < ada, ["Ana", "Ada"])

# "Ana finished third-to-last" → With 7 participants, third-to-last is position 5
problem.addConstraint(lambda ana: ana == 5, ["Ana"])

# "Mel finished last" → Mel's rank == 7
problem.addConstraint(lambda mel: mel == 7, ["Mel"])

# "Amy finished third" → Amy's rank == 3
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Dan",
    "C": "Ana",
    "D": "Mel",
    "E": "Ada",
    "F": "Eve",
    "G": "Amy"
}

# Find who has rank 2 (second place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
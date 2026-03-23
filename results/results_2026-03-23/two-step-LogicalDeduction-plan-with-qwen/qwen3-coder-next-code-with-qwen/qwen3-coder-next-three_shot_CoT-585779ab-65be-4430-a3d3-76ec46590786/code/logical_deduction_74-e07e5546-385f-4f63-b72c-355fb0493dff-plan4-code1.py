from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) with consistent casing as in the problem statement
golfers = ["Ana", "Rob", "Amy", "Dan", "Joe"]

# Define domain: 1 = best (first place), 5 = worst (fifth place)
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraint that all golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Rob finished below Dan" → Rob's rank > Dan's rank
problem.addConstraint(lambda rob, dan: rob > dan, ["Rob", "Dan"])

# "Joe finished below Ana" → Joe's rank > Ana's rank
problem.addConstraint(lambda joe, ana: joe > ana, ["Joe", "Ana"])

# "Joe finished above Amy" → Joe's rank < Amy's rank
problem.addConstraint(lambda joe, amy: joe < amy, ["Joe", "Amy"])

# "Dan finished below Amy" → Dan's rank > Amy's rank
problem.addConstraint(lambda dan, amy: dan > amy, ["Dan", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Amy",
    "D": "Dan",
    "E": "Joe"
}

# Find who finished third (rank = 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
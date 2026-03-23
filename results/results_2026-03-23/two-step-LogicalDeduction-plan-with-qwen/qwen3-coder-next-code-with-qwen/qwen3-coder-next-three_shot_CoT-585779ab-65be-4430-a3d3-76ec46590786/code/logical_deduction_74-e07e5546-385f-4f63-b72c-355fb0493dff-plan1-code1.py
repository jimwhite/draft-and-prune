from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Ana", "Rob", "Amy", "Dan", "Joe"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Rob finished below Dan" → Rob's position > Dan's position
problem.addConstraint(lambda rob, dan: rob > dan, ["Rob", "Dan"])

# "Joe finished below Ana" → Joe's position > Ana's position
problem.addConstraint(lambda joe, ana: joe > ana, ["Joe", "Ana"])

# "Joe finished above Amy" → Joe's position < Amy's position
problem.addConstraint(lambda joe, amy: joe < amy, ["Joe", "Amy"])

# "Dan finished below Amy" → Dan's position > Amy's position
problem.addConstraint(lambda dan, amy: dan > amy, ["Dan", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Amy",
    "D": "Dan",
    "E": "Joe"
}

# Find which golfer has position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
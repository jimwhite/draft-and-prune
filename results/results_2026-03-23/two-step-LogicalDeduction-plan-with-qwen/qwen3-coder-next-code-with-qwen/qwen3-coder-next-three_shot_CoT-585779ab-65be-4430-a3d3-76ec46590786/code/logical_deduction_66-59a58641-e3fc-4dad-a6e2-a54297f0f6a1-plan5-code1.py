from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Joe", "Eve", "Mya", "Rob", "Dan"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Joe finished below Dan" → Joe's position > Dan's position
problem.addConstraint(lambda joe, dan: joe > dan, ["Joe", "Dan"])

# "Mya finished first" → Mya's position = 1
problem.addConstraint(lambda mya: mya == 1, ["Mya"])

# "Dan finished below Rob" → Dan's position > Rob's position
problem.addConstraint(lambda dan, rob: dan > rob, ["Dan", "Rob"])

# "Eve finished above Rob" → Eve's position < Rob's position
problem.addConstraint(lambda eve, rob: eve < rob, ["Eve", "Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Eve",
    "C": "Mya",
    "D": "Rob",
    "E": "Dan"
}

# Find which golfer finished last (position 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
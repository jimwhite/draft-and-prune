from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = best)
golfers = ["ana", "rob", "amy", "dan", "joe"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraint that all golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Rob finished below Dan" → rob > dan
problem.addConstraint(lambda rob, dan: rob > dan, ["rob", "dan"])

# "Joe finished below Ana" → joe > ana
problem.addConstraint(lambda joe, ana: joe > ana, ["joe", "ana"])

# "Joe finished above Amy" → joe < amy
problem.addConstraint(lambda joe, amy: joe < amy, ["joe", "amy"])

# "Dan finished below Amy" → dan > amy
problem.addConstraint(lambda dan, amy: dan > amy, ["dan", "amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "ana",
    "B": "rob",
    "C": "amy",
    "D": "dan",
    "E": "joe"
}

# Find which golfer has position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
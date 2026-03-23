from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions 1-5, where 1 is best)
golfers = ["Rob", "Eve", "Eli", "Amy", "Dan"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished second
problem.addConstraint(lambda dan: dan == 2, ["Dan"])

# Amy finished below Eve (Amy's position number > Eve's)
problem.addConstraint(lambda amy, eve: amy > eve, ["Amy", "Eve"])

# Dan finished above Eve (Dan's position number < Eve's)
problem.addConstraint(lambda dan, eve: dan < eve, ["Dan", "Eve"])

# Amy finished above Eli (Amy's position number < Eli's)
problem.addConstraint(lambda amy, eli: amy < eli, ["Amy", "Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Rob",
    "B": "Eve",
    "C": "Eli",
    "D": "Amy",
    "E": "Dan"
}

# Find which golfer finished third (position == 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
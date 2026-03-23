from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place, 7 = last)
golfers = ["Ada", "Ana", "Rob", "Amy", "Dan", "Joe", "Eli"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Eli finished below Amy" → Eli's position > Amy's position
problem.addConstraint(lambda amy, eli: amy < eli, ["Amy", "Eli"])

# "Ada finished third" → Ada's position == 3
problem.addConstraint(lambda ada: ada == 3, ["Ada"])

# "Amy finished below Rob" → Amy's position > Rob's position
problem.addConstraint(lambda rob, amy: rob < amy, ["Rob", "Amy"])

# "Dan finished last" → Dan's position == 7
problem.addConstraint(lambda dan: dan == 7, ["Dan"])

# "Rob finished second" → Rob's position == 2
problem.addConstraint(lambda rob: rob == 2, ["Rob"])

# "Ana finished fourth" → Ana's position == 4
problem.addConstraint(lambda ana: ana == 4, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Ada",
    "B": "Ana",
    "C": "Rob",
    "D": "Amy",
    "E": "Dan",
    "F": "Joe",
    "G": "Eli"
}

# Find who finished last (position 7) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
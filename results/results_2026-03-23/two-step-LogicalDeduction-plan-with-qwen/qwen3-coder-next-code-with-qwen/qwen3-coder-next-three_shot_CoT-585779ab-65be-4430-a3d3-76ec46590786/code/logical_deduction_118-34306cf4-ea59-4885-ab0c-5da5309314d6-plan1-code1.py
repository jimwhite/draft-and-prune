from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Eli", "Ada", "Amy", "Ana", "Eve", "Mel", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mel" → Ada's position < Mel's position
problem.addConstraint(lambda ada, mel: ada < mel, ["Ada", "Mel"])

# "Dan finished above Ada" → Dan's position < Ada's position
problem.addConstraint(lambda dan, ada: dan < ada, ["Dan", "Ada"])

# "Amy finished last" → Amy's position = 7
problem.addConstraint(lambda amy: amy == 7, ["Amy"])

# "Ana finished third-to-last" → position = 5 (since 7=last, 6=second-last, 5=third-last)
problem.addConstraint(lambda ana: ana == 5, ["Ana"])

# "Dan finished below Eli" → Dan's position > Eli's position
problem.addConstraint(lambda dan, eli: dan > eli, ["Dan", "Eli"])

# "Eve finished third" → Eve's position = 3
problem.addConstraint(lambda eve: eve == 3, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Eli",
    "B": "Ada",
    "C": "Amy",
    "D": "Ana",
    "E": "Eve",
    "F": "Mel",
    "G": "Dan"
}

# Find which golfer has position 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
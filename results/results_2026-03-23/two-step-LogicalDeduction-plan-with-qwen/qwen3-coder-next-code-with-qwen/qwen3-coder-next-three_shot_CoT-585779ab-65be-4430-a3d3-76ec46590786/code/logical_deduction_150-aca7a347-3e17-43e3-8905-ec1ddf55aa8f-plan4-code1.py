from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 is best)
golfers = ["Joe", "Dan", "Ada", "Amy", "Rob", "Mya", "Mel"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished below Amy" → Ada's rank > Amy's rank
problem.addConstraint(lambda ada, amy: ada > amy, ["Ada", "Amy"])

# "Joe finished below Dan" → Joe's rank > Dan's rank
problem.addConstraint(lambda joe, dan: joe > dan, ["Joe", "Dan"])

# "Dan finished below Ada" → Dan's rank > Ada's rank
problem.addConstraint(lambda dan, ada: dan > ada, ["Dan", "Ada"])

# "Mel finished third-to-last" → rank 5 (positions: 7=last, 6=second-last, 5=third-last)
problem.addConstraint(lambda mel: mel == 5, ["Mel"])

# "Amy finished third" → rank 3
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# "Rob finished below Mya" → Rob's rank > Mya's rank
problem.addConstraint(lambda rob, mya: rob > mya, ["Rob", "Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Dan",
    "C": "Ada",
    "D": "Amy",
    "E": "Rob",
    "F": "Mya",
    "G": "Mel"
}

# Find who has rank 2 (second place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
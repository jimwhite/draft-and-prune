from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Amy finished third"
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# "Joe finished last"
problem.addConstraint(lambda joe: joe == 7, ["Joe"])

# "Mya finished above Dan" (Mya's position number < Dan's position number)
problem.addConstraint(lambda mya, dan: mya < dan, ["Mya", "Dan"])

# "Eve finished fourth"
problem.addConstraint(lambda eve: eve == 4, ["Eve"])

# "Amy finished above Rob" (Amy's position number < Rob's position number)
problem.addConstraint(lambda amy, rob: amy < rob, ["Amy", "Rob"])

# "Ada finished third-to-last" (position 5 in a 7-person race: 7-2=5)
problem.addConstraint(lambda ada: ada == 5, ["Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Dan",
    "B": "Eve",
    "C": "Mya",
    "D": "Amy",
    "E": "Rob",
    "F": "Ada",
    "G": "Joe"
}

# Find who finished third (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
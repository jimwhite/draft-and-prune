from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7)
golfers = ["dan", "eve", "mya", "amy", "rob", "ada", "joe"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add explicit position constraints based on the statements
# Amy finished third
problem.addConstraint(lambda amy: amy == 3, ["amy"])
# Joe finished last
problem.addConstraint(lambda joe: joe == 7, ["joe"])
# Eve finished fourth
problem.addConstraint(lambda eve: eve == 4, ["eve"])
# Ada finished third-to-last (position 5 in a 7-person field)
problem.addConstraint(lambda ada: ada == 5, ["ada"])

# Add relative ordering constraints
# Mya finished above Dan (Mya's rank < Dan's rank)
problem.addConstraint(lambda mya, dan: mya < dan, ["mya", "dan"])
# Amy finished above Rob (Amy's rank < Rob's rank)
problem.addConstraint(lambda amy, rob: amy < rob, ["amy", "rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "dan",
    "B": "eve",
    "C": "mya",
    "D": "amy",
    "E": "rob",
    "F": "ada",
    "G": "joe"
}

# Find which golfer has rank 5 (third-to-last) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
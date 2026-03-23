from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["dan", "eve", "mya", "amy", "rob", "ada", "joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Amy finished third
problem.addConstraint(lambda amy: amy == 3, ["amy"])

# Joe finished last
problem.addConstraint(lambda joe: joe == 7, ["joe"])

# Eve finished fourth
problem.addConstraint(lambda eve: eve == 4, ["eve"])

# Ada finished third-to-last (position 5 in a 7-person race)
problem.addConstraint(lambda ada: ada == 5, ["ada"])

# Mya finished above Dan (mya < dan)
problem.addConstraint(lambda mya, dan: mya < dan, ["mya", "dan"])

# Amy finished above Rob (amy < rob)
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

# Find the golfer who finished second-to-last (position 6)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 6:
            print(letter)
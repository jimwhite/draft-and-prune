from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["dan", "eve", "mya", "amy", "rob", "ada", "joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Amy finished third"
problem.addConstraint(lambda amy: amy == 3, ["amy"])

# "Joe finished last"
problem.addConstraint(lambda joe: joe == 7, ["joe"])

# "Mya finished above Dan" (mya < dan)
problem.addConstraint(lambda mya, dan: mya < dan, ["mya", "dan"])

# "Eve finished fourth"
problem.addConstraint(lambda eve: eve == 4, ["eve"])

# "Amy finished above Rob" (amy < rob)
problem.addConstraint(lambda amy, rob: amy < rob, ["amy", "rob"])

# "Ada finished third-to-last" (position 5 in a 7-person field)
problem.addConstraint(lambda ada: ada == 5, ["ada"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "dan",
    "B": "eve",
    "C": "mya",
    "D": "amy",
    "E": "rob",
    "F": "ada",
    "G": "joe"
}

# Find who finished third (position 3) and print the corresponding letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions 1 to 7)
golfers = ["mya", "eli", "ana", "amy", "mel", "dan", "joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have unique finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Joe" → Amy's position > Joe's
problem.addConstraint(lambda amy, joe: amy > joe, ["amy", "joe"])

# "Dan finished above Mya" → Dan's position < Mya's
problem.addConstraint(lambda dan, mya: dan < mya, ["dan", "mya"])

# "Eli finished third"
problem.addConstraint(lambda eli: eli == 3, ["eli"])

# "Ana finished first"
problem.addConstraint(lambda ana: ana == 1, ["ana"])

# "Amy finished second-to-last" → position 6 (since last is 7)
problem.addConstraint(lambda amy: amy == 6, ["amy"])

# "Mya finished fourth"
problem.addConstraint(lambda mya: mya == 4, ["mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "mya",
    "B": "eli",
    "C": "ana",
    "D": "amy",
    "E": "mel",
    "F": "dan",
    "G": "joe"
}

# Find who finished second (position 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
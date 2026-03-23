from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 is first place)
golfers = ["Mya", "Eli", "Ana", "Amy", "Mel", "Dan", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Joe" → Amy's rank > Joe's rank
problem.addConstraint(lambda amy, joe: amy > joe, ["Amy", "Joe"])

# "Dan finished above Mya" → Dan's rank < Mya's rank
problem.addConstraint(lambda dan, mya: dan < mya, ["Dan", "Mya"])

# "Eli finished third"
problem.addConstraint(lambda eli: eli == 3, ["Eli"])

# "Ana finished first"
problem.addConstraint(lambda ana: ana == 1, ["Ana"])

# "Amy finished second-to-last" → rank = 6
problem.addConstraint(lambda amy: amy == 6, ["Amy"])

# "Mya finished fourth"
problem.addConstraint(lambda mya: mya == 4, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Mya",
    "B": "Eli",
    "C": "Ana",
    "D": "Amy",
    "E": "Mel",
    "F": "Dan",
    "G": "Joe"
}

# Find which golfer finished third-to-last (position 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
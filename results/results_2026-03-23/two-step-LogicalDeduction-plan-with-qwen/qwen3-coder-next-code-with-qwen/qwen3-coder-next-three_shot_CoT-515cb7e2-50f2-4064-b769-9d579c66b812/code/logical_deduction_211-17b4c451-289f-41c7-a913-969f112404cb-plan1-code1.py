from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = first place)
golfers = ["Mya", "Eli", "Ana", "Amy", "Mel", "Dan", "Joe"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Amy finished below Joe" → Amy's rank > Joe's rank
problem.addConstraint(lambda amy, joe: amy > joe, ["Amy", "Joe"])

# "Dan finished above Mya" → Dan's rank < Mya's rank
problem.addConstraint(lambda dan, mya: dan < mya, ["Dan", "Mya"])

# "Eli finished third" → Eli's rank == 3
problem.addConstraint(lambda eli: eli == 3, ["Eli"])

# "Ana finished first" → Ana's rank == 1
problem.addConstraint(lambda ana: ana == 1, ["Ana"])

# "Amy finished second-to-last" → Amy's rank == 6 (since last is 7)
problem.addConstraint(lambda amy: amy == 6, ["Amy"])

# "Mya finished fourth" → Mya's rank == 4
problem.addConstraint(lambda mya: mya == 4, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Determine third-to-last place (position 5 in a 7-golfer field)
choices = {
    "A": "Mya",
    "B": "Eli",
    "C": "Ana",
    "D": "Amy",
    "E": "Mel",
    "F": "Dan",
    "G": "Joe"
}

# Find which golfer has rank 5 (third-to-last)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
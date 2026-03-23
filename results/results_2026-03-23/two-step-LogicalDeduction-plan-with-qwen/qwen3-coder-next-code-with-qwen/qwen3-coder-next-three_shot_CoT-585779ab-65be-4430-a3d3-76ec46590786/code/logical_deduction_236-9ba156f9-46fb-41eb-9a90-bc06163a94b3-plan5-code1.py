from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["mya", "eli", "ana", "amy", "mel", "dan", "joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Amy finished below Joe" → amy > joe
problem.addConstraint(lambda amy, joe: amy > joe, ["amy", "joe"])

# "Dan finished above Mya" → dan < mya
problem.addConstraint(lambda dan, mya: dan < mya, ["dan", "mya"])

# "Eli finished third" → eli == 3
problem.addConstraint(lambda eli: eli == 3, ["eli"])

# "Ana finished first" → ana == 1
problem.addConstraint(lambda ana: ana == 1, ["ana"])

# "Amy finished second-to-last" → amy == 6 (in a 7-golfer field)
problem.addConstraint(lambda amy: amy == 6, ["amy"])

# "Mya finished fourth" → mya == 4
problem.addConstraint(lambda mya: mya == 4, ["mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map golfers to choice letters for second place
golfer_to_choice = {
    "mya": "A",
    "eli": "B",
    "ana": "C",
    "amy": "D",
    "mel": "E",
    "dan": "F",
    "joe": "G"
}

# Find who finished second (position 2)
for solution in solutions:
    for golfer, position in solution.items():
        if position == 2:
            print(golfer_to_choice[golfer])
from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["mya", "eli", "ana", "amy", "mel", "dan", "joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have different positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Amy finished below Joe" → amy > joe
problem.addConstraint(lambda amy, joe: amy > joe, ["amy", "joe"])

# 3. "Dan finished above Mya" → dan < mya
problem.addConstraint(lambda dan, mya: dan < mya, ["dan", "mya"])

# 4. "Eli finished third" → eli == 3
problem.addConstraint(lambda eli: eli == 3, ["eli"])

# 5. "Ana finished first" → ana == 1
problem.addConstraint(lambda ana: ana == 1, ["ana"])

# 6. "Amy finished second-to-last" → amy == 6
problem.addConstraint(lambda amy: amy == 6, ["amy"])

# 7. "Mya finished fourth" → mya == 4
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

# Find which golfer finished third-to-last (position 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Mya", "Eli", "Ana", "Amy", "Mel", "Dan", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Amy finished below Joe" → Amy's position > Joe's position
problem.addConstraint(lambda amy, joe: amy > joe, ["Amy", "Joe"])

# "Dan finished above Mya" → Dan's position < Mya's position
problem.addConstraint(lambda dan, mya: dan < mya, ["Dan", "Mya"])

# "Eli finished third" → Eli's position = 3
problem.addConstraint(lambda eli: eli == 3, ["Eli"])

# "Ana finished first" → Ana's position = 1
problem.addConstraint(lambda ana: ana == 1, ["Ana"])

# "Amy finished second-to-last" → Amy's position = 6
problem.addConstraint(lambda amy: amy == 6, ["Amy"])

# "Mya finished fourth" → Mya's position = 4
problem.addConstraint(lambda mya: mya == 4, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# For 7 golfers, third-to-last is position 5 (since last=7, second-to-last=6, third-to-last=5)
third_to_last_position = 5

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

# Find which golfer is in position 5 and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == third_to_last_position:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["mya", "eli", "ana", "amy", "mel", "dan", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Amy finished below Joe" → Amy's position > Joe's position
problem.addConstraint(lambda amy, joe: amy > joe, ["amy", "Joe"])

# "Dan finished above Mya" → Dan's position < Mya's position
problem.addConstraint(lambda dan, mya: dan < mya, ["dan", "mya"])

# "Eli finished third" → Eli's position = 3
problem.addConstraint(lambda eli: eli == 3, ["eli"])

# "Ana finished first" → Ana's position = 1
problem.addConstraint(lambda ana: ana == 1, ["ana"])

# "Amy finished second-to-last" → Amy's position = 6
problem.addConstraint(lambda amy: amy == 6, ["amy"])

# "Mya finished fourth" → Mya's position = 4
problem.addConstraint(lambda mya: mya == 4, ["mya"])

# Solve the problem
solutions = problem.getSolutions()

# Determine third-to-last position (for 7 golfers, this is position 5)
third_to_last_position = 5

# Map choice letters to golfer names
choices = {
    "A": "mya",
    "B": "eli",
    "C": "ana",
    "D": "amy",
    "E": "mel",
    "F": "dan",
    "G": "Joe"
}

# Find which golfer is in position 5 and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == third_to_last_position:
            print(letter)
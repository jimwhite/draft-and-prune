from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) with exact names as given
golfers = ["mya", "eli", "ana", "amy", "mel", "dan", "Joe"]

# Define domain: positions 1 to 7 (1 = first place, 7 = last place)
positions = range(1, 8)

# Add variables to the problem
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Amy finished below Joe" → amy > joe
problem.addConstraint(lambda amy, joe: amy > joe, ["amy", "Joe"])

# "Dan finished above Mya" → dan < mya
problem.addConstraint(lambda dan, mya: dan < mya, ["dan", "mya"])

# "Eli finished third" → eli == 3
problem.addConstraint(lambda eli: eli == 3, ["eli"])

# "Ana finished first" → ana == 1
problem.addConstraint(lambda ana: ana == 1, ["ana"])

# "Amy finished second-to-last" → amy == 6
problem.addConstraint(lambda amy: amy == 6, ["amy"])

# "Mya finished fourth" → mya == 4
problem.addConstraint(lambda mya: mya == 4, ["mya"])

# Solve the problem
solutions = problem.getSolutions()

# With 7 golfers, third-to-last is position 5 (since 7 - 3 + 1 = 5)
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

# Find which golfer is in position 5
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == third_to_last_position:
            print(letter)
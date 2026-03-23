from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["mya", "eli", "ana", "amy", "mel", "dan", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Amy finished below Joe" → amy > Joe
problem.addConstraint(lambda amy, Joe: amy > Joe, ["amy", "Joe"])

# "Dan finished above Mya" → dan < mya
problem.addConstraint(lambda dan, mya: dan < mya, ["dan", "mya"])

# "Eli finished third" → eli == 3
problem.addConstraint(lambda eli: eli == 3, ["eli"])

# "Ana finished first" → ana == 1
problem.addConstraint(lambda ana: ana == 1, ["ana"])

# "Amy finished second-to-last" → amy == 6 (with 7 golfers)
problem.addConstraint(lambda amy: amy == 6, ["amy"])

# "Mya finished fourth" → mya == 4
problem.addConstraint(lambda mya: mya == 4, ["mya"])

# Solve the problem
solutions = problem.getSolutions()

# Determine third-to-last position (position 5 in a 7-golfer race)
third_to_last = 5

# Map choice letters to golfers
choices = {
    'A': "mya",
    'B': "eli",
    'C': "ana",
    'D': "amy",
    'E': "mel",
    'F': "dan",
    'G': "Joe"
}

# Find which golfer is in position 5 and print the corresponding choice letter
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == third_to_last:
            print(letter)
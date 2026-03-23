from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=fifth)
golfers = ["amy", "dan", "mya", "eli", "mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Mya finished first
problem.addConstraint(lambda mya: mya == 1, ["mya"])

# Dan finished last
problem.addConstraint(lambda dan: dan == 5, ["dan"])

# Amy finished above Mel (Amy's position number is smaller than Mel's)
problem.addConstraint(lambda amy, mel: amy < mel, ["amy", "mel"])

# Amy finished below Eli (Eli's position number is smaller than Amy's)
problem.addConstraint(lambda eli, amy: eli < amy, ["eli", "amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "amy",
    "B": "dan",
    "C": "mya",
    "D": "eli",
    "E": "mel"
}

# Find which golfer has position 1 (first place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
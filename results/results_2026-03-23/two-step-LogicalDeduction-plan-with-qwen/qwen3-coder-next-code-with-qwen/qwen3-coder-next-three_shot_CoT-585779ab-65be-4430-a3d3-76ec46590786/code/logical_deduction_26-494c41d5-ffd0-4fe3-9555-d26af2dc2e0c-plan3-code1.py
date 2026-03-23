from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["amy", "dan", "mya", "eli", "mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Amy finished above Mel: amy's position < mel's position
problem.addConstraint(lambda amy, mel: amy < mel, ["amy", "mel"])

# Mya finished first: mya's position = 1
problem.addConstraint(lambda mya: mya == 1, ["mya"])

# Amy finished below Eli: amy's position > eli's position
problem.addConstraint(lambda amy, eli: amy > eli, ["amy", "eli"])

# Dan finished last: dan's position = 5
problem.addConstraint(lambda dan: dan == 5, ["dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "amy",
    "B": "dan",
    "C": "mya",
    "D": "eli",
    "E": "mel"
}

# Find who finished first (position = 1)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 1:
            print(letter)
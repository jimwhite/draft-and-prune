from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 3, where 1=best rank, 3=worst/last)
golfers = ["amy", "eli", "eve"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finish positions
problem.addConstraint(AllDifferentConstraint())

# "Eve finished above Amy" → Eve's position number is smaller than Amy's
problem.addConstraint(lambda eve, amy: eve < amy, ["eve", "amy"])

# "Eli finished below Amy" → Eli's position number is larger than Amy's
problem.addConstraint(lambda amy, eli: amy < eli, ["amy", "eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "amy",
    "B": "eli",
    "C": "eve"
}

# Find who finished last (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
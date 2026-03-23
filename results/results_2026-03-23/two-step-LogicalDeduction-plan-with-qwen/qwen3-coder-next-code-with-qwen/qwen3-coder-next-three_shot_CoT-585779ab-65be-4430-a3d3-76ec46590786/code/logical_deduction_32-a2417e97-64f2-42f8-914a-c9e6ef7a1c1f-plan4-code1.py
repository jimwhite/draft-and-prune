from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1-5, where 1 is best)
golfers = ["rob", "eve", "eli", "amy", "dan"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished second
problem.addConstraint(lambda dan: dan == 2, ["dan"])

# Amy finished below Eve (Amy's position > Eve's position)
problem.addConstraint(lambda amy, eve: amy > eve, ["amy", "eve"])

# Dan finished above Eve (Dan's position < Eve's position)
problem.addConstraint(lambda dan, eve: dan < eve, ["dan", "eve"])

# Amy finished above Eli (Amy's position < Eli's position)
problem.addConstraint(lambda amy, eli: amy < eli, ["amy", "eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "rob",
    "B": "eve",
    "C": "eli",
    "D": "amy",
    "E": "dan"
}

# Find which golfer finished third (position == 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=best, 3=worst)
golfers = ["amy", "eli", "eve"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# "Eve finished above Amy" → eve's position < amy's position
problem.addConstraint(lambda eve, amy: eve < amy, ["eve", "amy"])

# "Eli finished below Amy" → amy's position < eli's position
problem.addConstraint(lambda amy, eli: amy < eli, ["amy", "eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "amy",
    "B": "eli",
    "C": "eve"
}

# Find which golfer has rank 3 (last place)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)
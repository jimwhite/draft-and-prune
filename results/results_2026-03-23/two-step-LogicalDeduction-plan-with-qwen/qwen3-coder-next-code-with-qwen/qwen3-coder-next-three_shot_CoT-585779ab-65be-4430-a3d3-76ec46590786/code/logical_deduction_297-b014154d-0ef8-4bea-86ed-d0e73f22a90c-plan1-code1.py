from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=last)
golfers = ["amy", "eli", "eve"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints based on the statements
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Eve finished above Amy" means Eve's position is less than Amy's
problem.addConstraint(lambda eve, amy: eve < amy, ["eve", "amy"])

# "Eli finished below Amy" means Eli's position is greater than Amy's
problem.addConstraint(lambda eli, amy: eli > amy, ["eli", "amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names for the "finished last" question (position 3)
choices = {
    "A": "amy",
    "B": "eli",
    "C": "eve"
}

# Find which golfer has position 3 (last place) and print the corresponding letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Rob", "Amy", "Eve", "Mya", "Ana"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Mya finished below Rob" → Mya's position > Rob's position
problem.addConstraint(lambda mya, rob: mya > rob, ["Mya", "Rob"])

# "Ana finished below Eve" → Ana's position > Eve's position
problem.addConstraint(lambda ana, eve: ana > eve, ["Ana", "Eve"])

# "Amy finished second" → Amy's position is exactly 2
problem.addConstraint(lambda amy: amy == 2, ["Amy"])

# "Eve finished below Mya" → Eve's position > Mya's position
problem.addConstraint(lambda eve, mya: eve > mya, ["Eve", "Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names for second-to-last position (position 4)
choices = {
    "A": "Rob",
    "B": "Amy",
    "C": "Eve",
    "D": "Mya",
    "E": "Ana"
}

# Find which golfer is in position 4 (second-to-last)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)
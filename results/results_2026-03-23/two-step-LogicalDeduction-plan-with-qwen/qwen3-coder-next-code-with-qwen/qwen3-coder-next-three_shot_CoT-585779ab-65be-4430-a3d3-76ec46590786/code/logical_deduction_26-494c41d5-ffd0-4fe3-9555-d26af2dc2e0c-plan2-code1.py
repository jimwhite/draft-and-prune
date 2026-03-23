from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Amy", "Dan", "Mya", "Eli", "Mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have distinct positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished above Mel" → Amy's position < Mel's position
problem.addConstraint(lambda Amy, Mel: Amy < Mel, ["Amy", "Mel"])

# "Mya finished first" → Mya's position = 1
problem.addConstraint(lambda Mya: Mya == 1, ["Mya"])

# "Amy finished below Eli" → Amy's position > Eli's position (Eli < Amy)
problem.addConstraint(lambda Eli, Amy: Eli < Amy, ["Eli", "Amy"])

# "Dan finished last" → Dan's position = 5
problem.addConstraint(lambda Dan: Dan == 5, ["Dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Amy",
    "B": "Dan",
    "C": "Mya",
    "D": "Eli",
    "E": "Mel"
}

# Find which golfer has position 1 (first place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
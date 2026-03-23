from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Amy", "Dan", "Mya", "Eli", "Mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Amy finished above Mel" -> Amy's position < Mel's position
problem.addConstraint(lambda amy, mel: amy < mel, ["Amy", "Mel"])

# "Mya finished first" -> Mya's position = 1
problem.addConstraint(lambda mya: mya == 1, ["Mya"])

# "Amy finished below Eli" -> Amy's position > Eli's position
problem.addConstraint(lambda amy, eli: amy > eli, ["Amy", "Eli"])

# "Dan finished last" -> Dan's position = 5
problem.addConstraint(lambda dan: dan == 5, ["Dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Amy",
    "B": "Dan",
    "C": "Mya",
    "D": "Eli",
    "E": "Mel"
}

# Find which golfer finished first (position 1)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 1:
            print(letter)
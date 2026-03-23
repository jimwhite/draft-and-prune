from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 is first place)
golfers = ["Ada", "Eli", "Amy", "Joe", "Mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Ada finished above Eli: Ada's position < Eli's position
problem.addConstraint(lambda Ada, Eli: Ada < Eli, ["Ada", "Eli"])

# Amy finished below Mel: Amy's position > Mel's position
problem.addConstraint(lambda Amy, Mel: Amy > Mel, ["Amy", "Mel"])

# Ada finished second: Ada's position == 2
problem.addConstraint(lambda Ada: Ada == 2, ["Ada"])

# Mel finished below Eli: Mel's position > Eli's position
problem.addConstraint(lambda Mel, Eli: Mel > Eli, ["Mel", "Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Ada",
    "B": "Eli",
    "C": "Amy",
    "D": "Joe",
    "E": "Mel"
}

# Find who finished second (position 2) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
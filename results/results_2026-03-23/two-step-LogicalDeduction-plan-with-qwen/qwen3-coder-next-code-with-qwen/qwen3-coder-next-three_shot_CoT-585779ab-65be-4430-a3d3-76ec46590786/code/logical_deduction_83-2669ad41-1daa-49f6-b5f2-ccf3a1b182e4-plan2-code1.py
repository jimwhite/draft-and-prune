from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Ada", "Eli", "Amy", "Joe", "Mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Ada finished above Eli: Ada's position < Eli's position
problem.addConstraint(lambda ada, eli: ada < eli, ["Ada", "Eli"])

# Amy finished below Mel: Amy's position > Mel's position
problem.addConstraint(lambda amy, mel: amy > mel, ["Amy", "Mel"])

# Ada finished second
problem.addConstraint(lambda ada: ada == 2, ["Ada"])

# Mel finished below Eli: Mel's position > Eli's position
problem.addConstraint(lambda mel, eli: mel > eli, ["Mel", "Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Since all choices are about who finished second, and we know Ada finished second,
# the correct answer is A) Ada finished second.
# We can verify this by checking that in all solutions, Ada's position is 2.
for solution in solutions:
    if solution["Ada"] == 2:
        print("A")
        break
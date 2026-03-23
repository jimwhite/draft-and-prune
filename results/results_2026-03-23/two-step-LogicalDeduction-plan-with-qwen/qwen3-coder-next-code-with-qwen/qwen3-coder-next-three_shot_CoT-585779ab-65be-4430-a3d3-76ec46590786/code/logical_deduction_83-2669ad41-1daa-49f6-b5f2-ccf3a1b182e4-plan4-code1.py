from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 is best)
golfers = ["Ada", "Eli", "Amy", "Joe", "Mel"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# Ada finished above Eli: Ada's rank < Eli's rank
problem.addConstraint(lambda ada, eli: ada < eli, ["Ada", "Eli"])

# Amy finished below Mel: Amy's rank > Mel's rank
problem.addConstraint(lambda amy, mel: amy > mel, ["Amy", "Mel"])

# Ada finished second
problem.addConstraint(lambda ada: ada == 2, ["Ada"])

# Mel finished below Eli: Mel's rank > Eli's rank
problem.addConstraint(lambda mel, eli: mel > eli, ["Mel", "Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Check which choice is true (which golfer has rank 2)
for solution in solutions:
    if solution["Ada"] == 2:
        print("A")
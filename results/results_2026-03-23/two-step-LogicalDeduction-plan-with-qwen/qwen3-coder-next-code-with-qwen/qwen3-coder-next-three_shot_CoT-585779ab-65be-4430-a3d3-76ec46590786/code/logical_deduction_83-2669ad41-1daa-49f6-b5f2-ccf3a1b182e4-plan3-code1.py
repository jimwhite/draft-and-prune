from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first, 5 = fifth)
golfers = ["ada", "eli", "amy", "joe", "mel"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Ada finished above Eli: ada < eli
problem.addConstraint(lambda ada, eli: ada < eli, ["ada", "eli"])

# Amy finished below Mel: amy > mel
problem.addConstraint(lambda amy, mel: amy > mel, ["amy", "mel"])

# Ada finished second: ada == 2
problem.addConstraint(lambda ada: ada == 2, ["ada"])

# Mel finished below Eli: mel > eli
problem.addConstraint(lambda mel, eli: mel > eli, ["mel", "eli"])

# Solve the problem
solutions = problem.getSolutions()

# Since Ada is constrained to be second, choice A is automatically correct
print("A")
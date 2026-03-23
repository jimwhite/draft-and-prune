from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Joe", "Dan", "Ana", "Mel", "Ada", "Eve", "Amy"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Eve finished above Amy" → Eve's position < Amy's position
problem.addConstraint(lambda eve, amy: eve < amy, ["Eve", "Amy"])

# "Dan finished second" → Dan's position = 2
problem.addConstraint(lambda dan: dan == 2, ["Dan"])

# "Ada finished below Ana" → Ana's position < Ada's position
problem.addConstraint(lambda ana, ada: ana < ada, ["Ana", "Ada"])

# "Ana finished third-to-last" → In 7 golfers, third-to-last = position 5
problem.addConstraint(lambda ana: ana == 5, ["Ana"])

# "Mel finished last" → Mel's position = 7
problem.addConstraint(lambda mel: mel == 7, ["Mel"])

# "Amy finished third" → Amy's position = 3
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Find who finished second (position 2)
for solution in solutions:
    for golfer, position in solution.items():
        if position == 2:
            # Map to the choices: B) Dan finished second.
            print("B")
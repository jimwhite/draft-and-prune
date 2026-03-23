from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions 1 to 3)
golfers = ["Ana", "Dan", "Mel"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished second (position 2)
problem.addConstraint(lambda dan: dan == 2, ["Dan"])

# Mel finished first (position 1)
problem.addConstraint(lambda mel: mel == 1, ["Mel"])

# Solve the problem
solutions = problem.getSolutions()

# Get the unique solution
solution = solutions[0]

# Determine which golfer finished first (position 1)
first_place_golfer = None
for golfer, pos in solution.items():
    if pos == 1:
        first_place_golfer = golfer
        break

# Map to the correct choice letter
if first_place_golfer == "Ana":
    print("A")
elif first_place_golfer == "Dan":
    print("B")
elif first_place_golfer == "Mel":
    print("C")
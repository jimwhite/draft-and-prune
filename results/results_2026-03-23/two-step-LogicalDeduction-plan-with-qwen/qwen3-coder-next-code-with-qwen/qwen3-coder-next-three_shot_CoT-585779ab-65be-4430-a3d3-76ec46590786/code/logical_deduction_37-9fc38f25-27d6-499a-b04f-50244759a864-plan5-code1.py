from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=fifth)
golfers = ["Joe", "Ana", "Amy", "Mya", "Eve"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished last (position 5)
problem.addConstraint(lambda Joe: Joe == 5, ["Joe"])

# Ana finished second (position 2)
problem.addConstraint(lambda Ana: Ana == 2, ["Ana"])

# Mya finished second-to-last (position 4)
problem.addConstraint(lambda Mya: Mya == 4, ["Mya"])

# Eve finished below Amy (Eve's position > Amy's position)
problem.addConstraint(lambda Amy, Eve: Amy < Eve, ["Amy", "Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Find who finished first (position 1)
first_place_golfer = None
for solution in solutions:
    for golfer, position in solution.items():
        if position == 1:
            first_place_golfer = golfer
            break

# Map to choices
choices = {
    "A": "Joe",
    "B": "Ana",
    "C": "Amy",
    "D": "Mya",
    "E": "Eve"
}

# Determine which choice corresponds to the golfer in first place
for letter, golfer_name in choices.items():
    if golfer_name == first_place_golfer:
        print(letter)
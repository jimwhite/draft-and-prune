from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have unique positions
problem.addConstraint(AllDifferentConstraint())

# Amy finished third
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# Joe finished last
problem.addConstraint(lambda Joe: Joe == 7, ["Joe"])

# Eve finished fourth
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# Ada finished third-to-last (position 5 in a field of 7)
problem.addConstraint(lambda Ada: Ada == 5, ["Ada"])

# Mya finished above Dan (Mya's position < Dan's position)
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ["Mya", "Dan"])

# Amy finished above Rob (Amy's position < Rob's position)
problem.addConstraint(lambda Amy, Rob: Amy < Rob, ["Amy", "Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Dan",
    "B": "Eve",
    "C": "Mya",
    "D": "Amy",
    "E": "Rob",
    "F": "Ada",
    "G": "Joe"
}

# Find which golfer is in position 5 (third-to-last)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Amy finished third
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# Joe finished last
problem.addConstraint(lambda Joe: Joe == 7, ["Joe"])

# Mya finished above Dan (Mya's position number < Dan's position number)
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ["Mya", "Dan"])

# Eve finished fourth
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# Amy finished above Rob (Amy's position number < Rob's position number)
problem.addConstraint(lambda Amy, Rob: Amy < Rob, ["Amy", "Rob"])

# Ada finished third-to-last (in 7 positions, third-to-last is position 5)
problem.addConstraint(lambda Ada: Ada == 5, ["Ada"])

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

# Find which golfer finished fourth (position 4)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)
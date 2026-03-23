from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Amy", "Eve", "Ada", "Rob", "Dan", "Mel", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have distinct positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished third
problem.addConstraint(lambda Joe: Joe == 3, ["Joe"])

# Dan finished last (position 7)
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])

# Eve finished first (position 1)
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# Mel finished below Rob (Mel's position > Rob's position)
problem.addConstraint(lambda Mel, Rob: Mel > Rob, ["Mel", "Rob"])

# Ada finished above Joe (Ada's position < Joe's position = 3)
problem.addConstraint(lambda Ada: Ada < 3, ["Ada"])

# Rob finished third-to-last (position = 7 - 3 + 1 = 5)
problem.addConstraint(lambda Rob: Rob == 5, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Amy",
    "B": "Eve",
    "C": "Ada",
    "D": "Rob",
    "E": "Dan",
    "F": "Mel",
    "G": "Joe"
}

# Find who finished fourth (position 4)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)
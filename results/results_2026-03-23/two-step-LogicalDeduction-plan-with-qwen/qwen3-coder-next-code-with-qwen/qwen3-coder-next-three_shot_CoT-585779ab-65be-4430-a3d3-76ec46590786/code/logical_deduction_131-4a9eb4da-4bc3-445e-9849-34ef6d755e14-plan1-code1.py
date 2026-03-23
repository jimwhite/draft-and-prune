from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Rob finished first
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# Eve finished last
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# Dan finished above Ada (Dan's position < Ada's position)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# Mel finished above Mya (Mel's position < Mya's position)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# Joe finished second-to-last (position 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# Mya finished third (position 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map golfers to choice letters
choice_map = {
    "Joe": "A",
    "Mel": "B",
    "Mya": "C",
    "Eve": "D",
    "Rob": "E",
    "Ada": "F",
    "Dan": "G"
}

# Find which golfer is in position 3
for solution in solutions:
    for golfer, pos in solution.items():
        if pos == 3:
            print(choice_map[golfer])
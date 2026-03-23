from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Ada", "Ana", "Rob", "Amy", "Dan", "Joe", "Eli"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add explicit position constraints based on the statements
# "Ada finished third"
problem.addConstraint(lambda Ada: Ada == 3, ["Ada"])
# "Dan finished last"
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])
# "Rob finished second"
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])
# "Ana finished fourth"
problem.addConstraint(lambda Ana: Ana == 4, ["Ana"])

# Add relative position constraints
# "Eli finished below Amy" → Eli > Amy
problem.addConstraint(lambda Amy, Eli: Amy < Eli, ["Amy", "Eli"])
# "Amy finished below Rob" → Amy > Rob
problem.addConstraint(lambda Rob, Amy: Rob < Amy, ["Rob", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map golfers to choice letters
golfer_to_choice = {
    "Ada": "A",
    "Ana": "B",
    "Rob": "C",
    "Amy": "D",
    "Dan": "E",
    "Joe": "F",
    "Eli": "G"
}

# Find the golfer who finished last (position 7)
for solution in solutions:
    for golfer, position in solution.items():
        if position == 7:
            print(golfer_to_choice[golfer])
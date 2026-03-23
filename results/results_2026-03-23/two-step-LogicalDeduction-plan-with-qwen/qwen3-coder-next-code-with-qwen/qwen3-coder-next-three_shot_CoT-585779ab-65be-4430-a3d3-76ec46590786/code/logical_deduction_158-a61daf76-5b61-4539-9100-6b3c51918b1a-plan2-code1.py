from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Amy finished third"
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# "Joe finished last"
problem.addConstraint(lambda Joe: Joe == 7, ["Joe"])

# "Mya finished above Dan" (Mya < Dan)
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ["Mya", "Dan"])

# "Eve finished fourth"
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# "Amy finished above Rob" (Amy < Rob)
problem.addConstraint(lambda Amy, Rob: Amy < Rob, ["Amy", "Rob"])

# "Ada finished third-to-last" (position 5 in a 7-person race)
problem.addConstraint(lambda Ada: Ada == 5, ["Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Find who finished fourth (position 4)
for solution in solutions:
    for golfer, position in solution.items():
        if position == 4:
            # Map the golfer name to the corresponding choice letter
            if golfer == "Eve":
                print("B")
            break
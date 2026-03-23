from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Amy finished third
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# Joe finished last
problem.addConstraint(lambda joe: joe == 7, ["Joe"])

# Mya finished above Dan (Mya's position < Dan's position)
problem.addConstraint(lambda mya, dan: mya < dan, ["Mya", "Dan"])

# Eve finished fourth
problem.addConstraint(lambda eve: eve == 4, ["Eve"])

# Amy finished above Rob (Amy's position < Rob's position)
problem.addConstraint(lambda amy, rob: amy < rob, ["Amy", "Rob"])

# Ada finished third-to-last (position 5 in a 7-person race)
problem.addConstraint(lambda ada: ada == 5, ["Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know Amy is fixed at position 3 by the constraint, 
# the correct answer is directly D) Amy finished third.
# But to follow the plan and verify with the solution:
for solution in solutions:
    # Check who is at position 3
    for golfer, pos in solution.items():
        if pos == 3:
            # Map to the choices
            if golfer == "Amy":
                print("D")
            break
from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 3, where 1 = first/highest)
golfers = ["ana", "rob", "Joe"]
ranks = [1, 2, 3]
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers must have distinct ranks
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana: Joe's rank < Ana's rank
problem.addConstraint(lambda Joe, ana: Joe < ana, ["Joe", "ana"])

# Rob finished above Joe: Rob's rank < Joe's rank
problem.addConstraint(lambda rob, Joe: rob < Joe, ["rob", "Joe"])

# Solve the problem
solutions = problem.getSolutions()

# Find who finished second (rank = 2)
for solution in solutions:
    for golfer, rank in solution.items():
        if rank == 2:
            # Map the golfer to the correct choice letter
            if golfer == "rob":
                print("B")
            elif golfer == "ana":
                print("A")
            elif golfer == "Joe":
                print("C")
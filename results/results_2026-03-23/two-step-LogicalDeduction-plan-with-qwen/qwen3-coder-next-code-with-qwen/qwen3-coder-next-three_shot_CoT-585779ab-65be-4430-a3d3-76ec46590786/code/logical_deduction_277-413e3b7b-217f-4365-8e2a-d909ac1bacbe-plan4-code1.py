from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Eve", "Amy", "Rob"]
ranks = range(1, 4)  # 1=first, 2=second, 3=third
problem.addVariables(golfers, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# Amy finished above Rob → Amy's rank < Rob's rank
problem.addConstraint(lambda amy, rob: amy < rob, ("Amy", "Rob"))

# Eve finished above Amy → Eve's rank < Amy's rank
problem.addConstraint(lambda eve, amy: eve < amy, ("Eve", "Amy"))

# Solve the problem
solutions = problem.getSolutions()

# Find who finished second (rank = 2)
for solution in solutions:
    for golfer, rank in solution.items():
        if rank == 2:
            if golfer == "Eve":
                print("A")
            elif golfer == "Amy":
                print("B")
            elif golfer == "Rob":
                print("C")
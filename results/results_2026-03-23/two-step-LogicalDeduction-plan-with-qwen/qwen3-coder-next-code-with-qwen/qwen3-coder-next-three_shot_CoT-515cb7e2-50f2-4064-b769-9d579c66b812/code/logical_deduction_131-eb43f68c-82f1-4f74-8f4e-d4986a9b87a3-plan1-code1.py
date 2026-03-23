from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = first place)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# Rob finished first
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# Eve finished last
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# Dan finished above Ada (Dan's rank < Ada's rank)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# Mel finished above Mya (Mel's rank < Mya's rank)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# Joe finished second-to-last (rank 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# Mya finished third (rank 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map golfers to choice letters
golfer_to_choice = {
    "Joe": "A",
    "Mel": "B",
    "Mya": "C",
    "Eve": "D",
    "Rob": "E",
    "Ada": "F",
    "Dan": "G"
}

# Find who finished third (rank == 3)
for solution in solutions:
    for golfer, rank in solution.items():
        if rank == 3:
            print(golfer_to_choice[golfer])
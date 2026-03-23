from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 = first, 5 = last)
golfers = ["Rob", "Amy", "Eve", "Mya", "Ana"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints based on the statements
# 1. All golfers have unique ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "Mya finished below Rob" → Mya's rank > Rob's rank
problem.addConstraint(lambda rob, mya: mya > rob, ["Rob", "Mya"])

# 3. "Ana finished below Eve" → Ana's rank > Eve's rank
problem.addConstraint(lambda eve, ana: ana > eve, ["Eve", "Ana"])

# 4. "Amy finished second" → Amy's rank == 2
problem.addConstraint(lambda amy: amy == 2, ["Amy"])

# 5. "Eve finished below Mya" → Eve's rank > Mya's rank
problem.addConstraint(lambda mya, eve: eve > mya, ["Mya", "Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names for second-to-last (rank 4)
choices = {
    "A": "Rob",
    "B": "Amy",
    "C": "Eve",
    "D": "Mya",
    "E": "Ana"
}

# Find which golfer has rank 4 (second-to-last)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)
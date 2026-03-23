from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 = first place, 5 = last)
golfers = ["Dan", "Amy", "Eve", "Ana", "Mya"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints based on the statements
# 1. All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# 2. Dan finished above Eve → Dan's rank < Eve's rank
problem.addConstraint(lambda d, e: d < e, ["Dan", "Eve"])

# 3. Dan finished below Mya → Mya's rank < Dan's rank
problem.addConstraint(lambda m, d: m < d, ["Mya", "Dan"])

# 4. Amy finished third → Amy's rank = 3
problem.addConstraint(lambda a: a == 3, ["Amy"])

# 5. Ana finished second-to-last → Ana's rank = 4
problem.addConstraint(lambda an: an == 4, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Dan",
    "B": "Amy",
    "C": "Eve",
    "D": "Ana",
    "E": "Mya"
}

# Find which golfer has rank 5 (last place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
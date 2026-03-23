from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 = first place)
golfers = ["Eve", "Rob", "Ana", "Eli", "Mya"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "Eli finished below Mya" → Eli's rank > Mya's rank
problem.addConstraint(lambda e, m: e > m, ("Eli", "Mya"))

# "Eve finished first" → Eve's rank = 1
problem.addConstraint(lambda e: e == 1, ["Eve"])

# "Ana finished below Eli" → Ana's rank > Eli's rank
problem.addConstraint(lambda a, e: a > e, ("Ana", "Eli"))

# "Rob finished second" → Rob's rank = 2
problem.addConstraint(lambda r: r == 2, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Eve",
    "B": "Rob",
    "C": "Ana",
    "D": "Eli",
    "E": "Mya"
}

# Find who finished third (rank = 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
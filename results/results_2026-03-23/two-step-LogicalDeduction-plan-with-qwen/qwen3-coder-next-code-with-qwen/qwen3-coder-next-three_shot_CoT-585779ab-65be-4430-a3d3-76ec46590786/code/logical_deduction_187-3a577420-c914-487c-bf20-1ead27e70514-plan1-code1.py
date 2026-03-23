from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 is first place)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have distinct rankings
problem.addConstraint(AllDifferentConstraint())

# Mya finished above Eli: Mya's rank < Eli's rank
problem.addConstraint(lambda mya, eli: mya < eli, ("Mya", "Eli"))

# Eve finished below Rob: Eve's rank > Rob's rank
problem.addConstraint(lambda eve, rob: eve > rob, ("Eve", "Rob"))

# Amy finished second
problem.addConstraint(lambda amy: amy == 2, ("Amy",))

# Rob finished below Dan: Rob's rank > Dan's rank
problem.addConstraint(lambda rob, dan: rob > dan, ("Rob", "Dan"))

# Ana finished second-to-last (rank 6)
problem.addConstraint(lambda ana: ana == 6, ("Ana",))

# Dan finished fourth (rank 4)
problem.addConstraint(lambda dan: dan == 4, ("Dan",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Eve",
    "B": "Ana",
    "C": "Amy",
    "D": "Dan",
    "E": "Eli",
    "F": "Rob",
    "G": "Mya"
}

# Find who finished last (rank 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Mya finished above Eli" → Mya's rank < Eli's rank
problem.addConstraint(lambda mya, eli: mya < eli, ("Mya", "Eli"))

# "Eve finished below Rob" → Rob's rank < Eve's rank
problem.addConstraint(lambda rob, eve: rob < eve, ("Rob", "Eve"))

# "Amy finished second" → Amy == 2
problem.addConstraint(lambda amy: amy == 2, ("Amy",))

# "Rob finished below Dan" → Dan's rank < Rob's rank
problem.addConstraint(lambda dan, rob: dan < rob, ("Dan", "Rob"))

# "Ana finished second-to-last" → In 7 positions, this is position 6
problem.addConstraint(lambda ana: ana == 6, ("Ana",))

# "Dan finished fourth" → Dan == 4
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

# Find which golfer has rank 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
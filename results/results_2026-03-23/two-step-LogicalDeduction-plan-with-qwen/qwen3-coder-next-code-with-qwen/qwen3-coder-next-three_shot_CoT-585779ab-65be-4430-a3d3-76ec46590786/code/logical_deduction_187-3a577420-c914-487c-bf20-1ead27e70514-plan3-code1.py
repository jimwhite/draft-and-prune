from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place, 7 = last)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the clues:
# "Mya finished above Eli" → mya < eli
problem.addConstraint(lambda mya, eli: mya < eli, ["Mya", "Eli"])

# "Eve finished below Rob" → rob < eve
problem.addConstraint(lambda rob, eve: rob < eve, ["Rob", "Eve"])

# "Amy finished second" → amy == 2
problem.addConstraint(lambda amy: amy == 2, ["Amy"])

# "Rob finished below Dan" → dan < rob
problem.addConstraint(lambda dan, rob: dan < rob, ["Dan", "Rob"])

# "Ana finished second-to-last" → ana == 6
problem.addConstraint(lambda ana: ana == 6, ["Ana"])

# "Dan finished fourth" → dan == 4
problem.addConstraint(lambda dan: dan == 4, ["Dan"])

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

# Find which golfer finished last (position 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
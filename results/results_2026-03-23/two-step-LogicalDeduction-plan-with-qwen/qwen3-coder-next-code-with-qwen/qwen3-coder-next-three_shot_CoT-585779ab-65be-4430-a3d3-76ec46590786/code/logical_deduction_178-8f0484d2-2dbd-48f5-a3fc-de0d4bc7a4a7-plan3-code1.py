from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1-7, where 1 is best)
golfers = ["eve", "ana", "amy", "dan", "eli", "rob", "mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Mya finished above Eli" → mya < eli
problem.addConstraint(lambda mya, eli: mya < eli, ["mya", "eli"])

# "Eve finished below Rob" → eve > rob
problem.addConstraint(lambda eve, rob: eve > rob, ["eve", "rob"])

# "Amy finished second" → amy == 2
problem.addConstraint(lambda amy: amy == 2, ["amy"])

# "Rob finished below Dan" → rob > dan
problem.addConstraint(lambda rob, dan: rob > dan, ["rob", "dan"])

# "Ana finished second-to-last" → ana == 6
problem.addConstraint(lambda ana: ana == 6, ["ana"])

# "Dan finished fourth" → dan == 4
problem.addConstraint(lambda dan: dan == 4, ["dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "eve",
    "B": "ana",
    "C": "amy",
    "D": "dan",
    "E": "eli",
    "F": "rob",
    "G": "mya"
}

# Find who finished third (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
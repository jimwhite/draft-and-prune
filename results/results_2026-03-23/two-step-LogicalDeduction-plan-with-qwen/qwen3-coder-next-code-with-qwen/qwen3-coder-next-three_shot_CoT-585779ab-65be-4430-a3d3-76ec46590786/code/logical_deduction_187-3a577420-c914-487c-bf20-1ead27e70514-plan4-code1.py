from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Mya finished above Eli" → Mya's position < Eli's position
problem.addConstraint(lambda mya, eli: mya < eli, ("Mya", "Eli"))

# "Eve finished below Rob" → Eve's position > Rob's position
problem.addConstraint(lambda eve, rob: eve > rob, ("Eve", "Rob"))

# "Amy finished second" → Amy's position = 2
problem.addConstraint(lambda amy: amy == 2, ("Amy",))

# "Rob finished below Dan" → Rob's position > Dan's position
problem.addConstraint(lambda rob, dan: rob > dan, ("Rob", "Dan"))

# "Ana finished second-to-last" → Ana's position = 6
problem.addConstraint(lambda ana: ana == 6, ("Ana",))

# "Dan finished fourth" → Dan's position = 4
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

# Find which golfer finished last (position 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
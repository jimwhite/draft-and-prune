from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1-7, where 1 is first place, 7 is last)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Mya finished above Eli" -> mya < eli
problem.addConstraint(lambda mya, eli: mya < eli, ("Mya", "Eli"))

# "Eve finished below Rob" -> eve > rob
problem.addConstraint(lambda eve, rob: eve > rob, ("Eve", "Rob"))

# "Amy finished second" -> amy == 2
problem.addConstraint(lambda amy: amy == 2, ("Amy",))

# "Rob finished below Dan" -> rob > dan
problem.addConstraint(lambda rob, dan: rob > dan, ("Rob", "Dan"))

# "Ana finished second-to-last" -> ana == 6
problem.addConstraint(lambda ana: ana == 6, ("Ana",))

# "Dan finished fourth" -> dan == 4
problem.addConstraint(lambda dan: dan == 4, ("Dan",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': "Eve",
    'B': "Ana",
    'C': "Amy",
    'D': "Dan",
    'E': "Eli",
    'F': "Rob",
    'G': "Mya"
}

# Find who finished last (position 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
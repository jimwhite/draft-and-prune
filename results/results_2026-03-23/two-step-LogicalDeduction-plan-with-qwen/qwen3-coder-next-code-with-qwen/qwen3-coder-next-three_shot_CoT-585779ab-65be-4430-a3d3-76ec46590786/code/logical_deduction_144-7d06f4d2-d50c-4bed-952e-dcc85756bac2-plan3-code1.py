from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Joe", "Dan", "Ada", "Amy", "Rob", "Mya", "Mel"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished below Amy" → amy < ada
problem.addConstraint(lambda amy, ada: amy < ada, ["Amy", "Ada"])

# "Joe finished below Dan" → dan < joe
problem.addConstraint(lambda dan, joe: dan < joe, ["Dan", "Joe"])

# "Dan finished below Ada" → ada < dan
problem.addConstraint(lambda ada, dan: ada < dan, ["Ada", "Dan"])

# "Mel finished third-to-last" → position 5 (since 7-2=5)
problem.addConstraint(lambda mel: mel == 5, ["Mel"])

# "Amy finished third" → amy == 3
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# "Rob finished below Mya" → mya < rob
problem.addConstraint(lambda mya, rob: mya < rob, ["Mya", "Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': "Joe",
    'B': "Dan",
    'C': "Ada",
    'D': "Amy",
    'E': "Rob",
    'F': "Mya",
    'G': "Mel"
}

# Find who finished first (position 1)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 1:
            print(letter)
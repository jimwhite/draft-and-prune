from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Joe", "Dan", "Ada", "Amy", "Rob", "Mya", "Mel"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraint that all golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the clues:
# "Ada finished below Amy" → Ada's position > Amy's position
problem.addConstraint(lambda ada, amy: ada > amy, ["Ada", "Amy"])

# "Joe finished below Dan" → Joe's position > Dan's position
problem.addConstraint(lambda joe, dan: joe > dan, ["Joe", "Dan"])

# "Dan finished below Ada" → Dan's position > Ada's position
problem.addConstraint(lambda dan, ada: dan > ada, ["Dan", "Ada"])

# "Mel finished third-to-last" → In a 7-person race, third-to-last is position 5
problem.addConstraint(lambda mel: mel == 5, ["Mel"])

# "Amy finished third" → Amy's position = 3
problem.addConstraint(lambda amy: amy == 3, ["Amy"])

# "Rob finished below Mya" → Rob's position > Mya's position
problem.addConstraint(lambda rob, mya: rob > mya, ["Rob", "Mya"])

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

# Find who finished second (position = 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
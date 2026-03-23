from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = best/first place)
golfers = ["Eli", "Ada", "Amy", "Ana", "Eve", "Mel", "Dan"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mel" → Ada's rank < Mel's rank
problem.addConstraint(lambda ada, mel: ada < mel, ["Ada", "Mel"])

# "Dan finished above Ada" → Dan's rank < Ada's rank
problem.addConstraint(lambda dan, ada: dan < ada, ["Dan", "Ada"])

# "Amy finished last" → Amy's rank = 7
problem.addConstraint(lambda amy: amy == 7, ["Amy"])

# "Ana finished third-to-last" → In a 7-golfer field, positions are:
# 1=1st, 2=2nd, 3=3rd, 4=4th, 5=5th (third-to-last), 6=6th, 7=7th
problem.addConstraint(lambda ana: ana == 5, ["Ana"])

# "Dan finished below Eli" → Dan's rank > Eli's rank (worse finish)
problem.addConstraint(lambda dan, eli: dan > eli, ["Dan", "Eli"])

# "Eve finished third" → Eve's rank = 3
problem.addConstraint(lambda eve: eve == 3, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': 'Eli',
    'B': 'Ada',
    'C': 'Amy',
    'D': 'Ana',
    'E': 'Eve',
    'F': 'Mel',
    'G': 'Dan'
}

# Find which golfer has rank 3 (third place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
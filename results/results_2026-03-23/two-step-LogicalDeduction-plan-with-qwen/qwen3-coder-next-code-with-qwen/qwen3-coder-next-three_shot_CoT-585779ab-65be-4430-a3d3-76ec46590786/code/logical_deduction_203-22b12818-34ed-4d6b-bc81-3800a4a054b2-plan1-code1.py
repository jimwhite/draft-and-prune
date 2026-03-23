from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = first, 7 = last)
golfers = ["Eli", "Eve", "Mel", "Joe", "Mya", "Rob", "Ada"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished above Mya" → Ada's rank < Mya's rank
problem.addConstraint(lambda ada, mya: ada < mya, ("Ada", "Mya"))

# "Eli finished below Joe" → Eli's rank > Joe's rank
problem.addConstraint(lambda eli, joe: eli > joe, ("Eli", "Joe"))

# "Eli finished above Eve" → Eli's rank < Eve's rank
problem.addConstraint(lambda eli, eve: eli < eve, ("Eli", "Eve"))

# "Ada finished second-to-last" → Ada's rank = 6
problem.addConstraint(lambda ada: ada == 6, ("Ada",))

# "Mel finished third" → Mel's rank = 3
problem.addConstraint(lambda mel: mel == 3, ("Mel",))

# "Rob finished fourth" → Rob's rank = 4
problem.addConstraint(lambda rob: rob == 4, ("Rob",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    'A': 'Eli',
    'B': 'Eve',
    'C': 'Mel',
    'D': 'Joe',
    'E': 'Mya',
    'F': 'Rob',
    'G': 'Ada'
}

# Find which golfer has rank 2 (finished second)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
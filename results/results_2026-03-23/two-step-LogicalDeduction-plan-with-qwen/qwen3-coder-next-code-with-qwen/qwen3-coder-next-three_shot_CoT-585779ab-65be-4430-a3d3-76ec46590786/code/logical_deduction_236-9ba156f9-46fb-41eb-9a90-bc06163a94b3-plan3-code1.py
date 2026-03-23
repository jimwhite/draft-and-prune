from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define the seven golfers as variables
golfers = ["Mya", "Eli", "Ana", "Amy", "Mel", "Dan", "Joe"]

# Define the domain as positions 1 to 7 (1 = first place, 7 = last place)
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Amy finished below Joe" → Amy's rank > Joe's rank
problem.addConstraint(lambda amy, joe: amy > joe, ["Amy", "Joe"])

# 3. "Dan finished above Mya" → Dan's rank < Mya's rank
problem.addConstraint(lambda dan, mya: dan < mya, ["Dan", "Mya"])

# 4. "Eli finished third" → Eli's position = 3
problem.addConstraint(lambda eli: eli == 3, ["Eli"])

# 5. "Ana finished first" → Ana's position = 1
problem.addConstraint(lambda ana: ana == 1, ["Ana"])

# 6. "Amy finished second-to-last" → Amy's position = 6 (since 7 is last)
problem.addConstraint(lambda amy: amy == 6, ["Amy"])

# 7. "Mya finished fourth" → Mya's position = 4
problem.addConstraint(lambda mya: mya == 4, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Mya",
    "B": "Eli",
    "C": "Ana",
    "D": "Amy",
    "E": "Mel",
    "F": "Dan",
    "G": "Joe"
}

# Find who finished second (position = 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
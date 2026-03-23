from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 is best, 7 is last)
golfers = ["Joe", "Rob", "Eli", "Dan", "Mya", "Ada", "Ana"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have unique positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's position < Ana's position)
problem.addConstraint(lambda joe, ana: joe < ana, ["Joe", "Ana"])

# Ana finished second-to-last (position 6)
problem.addConstraint(lambda ana: ana == 6, ["Ana"])

# Mya finished fourth (position 4)
problem.addConstraint(lambda mya: mya == 4, ["Mya"])

# Dan finished third (position 3)
problem.addConstraint(lambda dan: dan == 3, ["Dan"])

# Ada finished second (position 2)
problem.addConstraint(lambda ada: ada == 2, ["Ada"])

# Eli finished third-to-last (position 5)
problem.addConstraint(lambda eli: eli == 5, ["Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Rob",
    "C": "Eli",
    "D": "Dan",
    "E": "Mya",
    "F": "Ada",
    "G": "Ana"
}

# Find who finished last (position 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
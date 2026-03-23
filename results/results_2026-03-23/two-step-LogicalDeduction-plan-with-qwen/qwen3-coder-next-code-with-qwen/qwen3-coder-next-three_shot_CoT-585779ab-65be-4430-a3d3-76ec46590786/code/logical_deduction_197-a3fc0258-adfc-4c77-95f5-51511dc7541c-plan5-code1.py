from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Mel", "Rob", "Eli", "Dan", "Ana", "Ada", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Ana finished last (position 7)
problem.addConstraint(lambda ana: ana == 7, ["Ana"])

# Rob finished fourth (position 4)
problem.addConstraint(lambda rob: rob == 4, ["Rob"])

# Eli finished second (position 2)
problem.addConstraint(lambda eli: eli == 2, ["Eli"])

# Mya finished above Rob (mya < rob)
problem.addConstraint(lambda mya, rob: mya < rob, ["Mya", "Rob"])

# Dan finished above Mya (dan < mya)
problem.addConstraint(lambda dan, mya: dan < mya, ["Dan", "Mya"])

# Mel finished above Ada (mel < ada)
problem.addConstraint(lambda mel, ada: mel < ada, ["Mel", "Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Mel",
    "B": "Rob",
    "C": "Eli",
    "D": "Dan",
    "E": "Ana",
    "F": "Ada",
    "G": "Mya"
}

# Find who finished third (position 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)
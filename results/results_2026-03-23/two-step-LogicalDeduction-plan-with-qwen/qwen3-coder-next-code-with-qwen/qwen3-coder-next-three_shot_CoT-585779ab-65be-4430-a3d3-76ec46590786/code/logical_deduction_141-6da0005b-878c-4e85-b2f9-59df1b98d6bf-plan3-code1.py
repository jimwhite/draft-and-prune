from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place, 7 = last)
golfers = ["Joe", "Rob", "Eli", "Dan", "Mya", "Ada", "Ana"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Joe finished above Ana" → Joe's position < Ana's position
problem.addConstraint(lambda j, a: j < a, ["Joe", "Ana"])

# "Ana finished second-to-last" → Ana's position = 6
problem.addConstraint(lambda a: a == 6, ["Ana"])

# "Mya finished fourth" → Mya's position = 4
problem.addConstraint(lambda m: m == 4, ["Mya"])

# "Dan finished third" → Dan's position = 3
problem.addConstraint(lambda d: d == 3, ["Dan"])

# "Ada finished second" → Ada's position = 2
problem.addConstraint(lambda a: a == 2, ["Ada"])

# "Eli finished third-to-last" → In a 7-golfer race, third-to-last is position 5
problem.addConstraint(lambda e: e == 5, ["Eli"])

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

# Find which golfer finished last (position 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)
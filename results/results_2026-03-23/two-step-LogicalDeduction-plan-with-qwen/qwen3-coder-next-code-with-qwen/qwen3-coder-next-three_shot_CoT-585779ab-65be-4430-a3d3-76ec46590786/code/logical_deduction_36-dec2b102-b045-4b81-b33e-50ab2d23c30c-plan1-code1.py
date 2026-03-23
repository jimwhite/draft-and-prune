from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=last)
golfers = ["Dan", "Amy", "Eve", "Ana", "Mya"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished above Eve → Dan's position < Eve's position
problem.addConstraint(lambda d, e: d < e, ["Dan", "Eve"])

# Dan finished below Mya → Mya's position < Dan's position
problem.addConstraint(lambda m, d: m < d, ["Mya", "Dan"])

# Amy finished third
problem.addConstraint(lambda a: a == 3, ["Amy"])

# Ana finished second-to-last (position 4 in a 5-person field)
problem.addConstraint(lambda a: a == 4, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Dan",
    "B": "Amy",
    "C": "Eve",
    "D": "Ana",
    "E": "Mya"
}

# Find who finished last (position 5)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 5:
            print(letter)
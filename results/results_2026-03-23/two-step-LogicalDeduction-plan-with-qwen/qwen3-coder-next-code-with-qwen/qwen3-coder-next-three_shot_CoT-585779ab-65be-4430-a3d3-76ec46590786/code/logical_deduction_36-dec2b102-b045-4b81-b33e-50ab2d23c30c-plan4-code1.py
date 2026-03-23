from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first, 5 = last)
golfers = ["Dan", "Amy", "Eve", "Ana", "Mya"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have distinct positions
problem.addConstraint(AllDifferentConstraint())

# Dan finished above Eve: Dan < Eve
problem.addConstraint(lambda Dan, Eve: Dan < Eve, ("Dan", "Eve"))

# Dan finished below Mya: Mya < Dan
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ("Mya", "Dan"))

# Amy finished third
problem.addConstraint(lambda Amy: Amy == 3, ("Amy",))

# Ana finished second-to-last (position 4 in a 5-person race)
problem.addConstraint(lambda Ana: Ana == 4, ("Ana",))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfer names
choices = {
    "A": "Dan",
    "B": "Amy",
    "C": "Eve",
    "D": "Ana",
    "E": "Mya"
}

# Find who finished last (position 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
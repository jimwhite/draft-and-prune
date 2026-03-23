from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=last)
golfers = ["Dan", "Amy", "Eve", "Ana", "Mya"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints based on the problem description
# 1. All golfers must have unique positions
problem.addConstraint(AllDifferentConstraint())

# 2. "Dan finished above Eve" → Dan's position < Eve's position
problem.addConstraint(lambda Dan, Eve: Dan < Eve, ["Dan", "Eve"])

# 3. "Dan finished below Mya" → Mya's position < Dan's position
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ["Mya", "Dan"])

# 4. "Amy finished third" → Amy's position = 3
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# 5. "Ana finished second-to-last" → Ana's position = 4 (in a 5-person race)
problem.addConstraint(lambda Ana: Ana == 4, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names for the "finished last" question
choices = {
    "A": "Dan",
    "B": "Amy",
    "C": "Eve",
    "D": "Ana",
    "E": "Mya"
}

# Find which golfer has position 5 (last) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=last)
golfers = ["Joe", "Eve", "Mya", "Rob", "Dan"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Joe finished below Dan" → Joe's position > Dan's position
problem.addConstraint(lambda Joe, Dan: Joe > Dan, ["Joe", "Dan"])

# "Mya finished first" → Mya's position = 1
problem.addConstraint(lambda Mya: Mya == 1, ["Mya"])

# "Dan finished below Rob" → Dan's position > Rob's position
problem.addConstraint(lambda Dan, Rob: Dan > Rob, ["Dan", "Rob"])

# "Eve finished above Rob" → Eve's position < Rob's position
problem.addConstraint(lambda Eve, Rob: Eve < Rob, ["Eve", "Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Eve",
    "C": "Mya",
    "D": "Rob",
    "E": "Dan"
}

# Find who finished last (position 5) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)
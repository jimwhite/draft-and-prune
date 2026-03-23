from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first)
golfers = ["Joe", "Dan", "Ada", "Amy", "Rob", "Mya", "Mel"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Ada finished below Amy" → Amy's position < Ada's position
problem.addConstraint(lambda Amy, Ada: Amy < Ada, ["Amy", "Ada"])

# "Joe finished below Dan" → Dan's position < Joe's position
problem.addConstraint(lambda Dan, Joe: Dan < Joe, ["Dan", "Joe"])

# "Dan finished below Ada" → Ada's position < Dan's position
problem.addConstraint(lambda Ada, Dan: Ada < Dan, ["Ada", "Dan"])

# "Mel finished third-to-last" → position 5 (since 7 - 3 + 1 = 5)
problem.addConstraint(lambda Mel: Mel == 5, ["Mel"])

# "Amy finished third" → Amy's position is exactly 3
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# "Rob finished below Mya" → Mya's position < Rob's position
problem.addConstraint(lambda Mya, Rob: Mya < Rob, ["Mya", "Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Dan",
    "C": "Ada",
    "D": "Amy",
    "E": "Rob",
    "F": "Mya",
    "G": "Mel"
}

# Find who finished second (position 2)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 2:
            print(letter)
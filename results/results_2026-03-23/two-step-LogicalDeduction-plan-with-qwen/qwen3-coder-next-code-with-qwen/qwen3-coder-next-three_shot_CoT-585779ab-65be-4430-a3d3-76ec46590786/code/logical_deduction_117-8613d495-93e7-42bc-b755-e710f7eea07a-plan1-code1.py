from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place, 7 = last)
golfers = ["Dan", "Eve", "Mya", "Amy", "Rob", "Ada", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add AllDifferentConstraint to ensure each golfer has a unique position
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Amy finished third"
problem.addConstraint(lambda Amy: Amy == 3, ["Amy"])

# "Joe finished last"
problem.addConstraint(lambda Joe: Joe == 7, ["Joe"])

# "Mya finished above Dan" → Mya < Dan
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ["Mya", "Dan"])

# "Eve finished fourth"
problem.addConstraint(lambda Eve: Eve == 4, ["Eve"])

# "Amy finished above Rob" → Amy < Rob (and since Amy == 3, this means Rob > 3)
problem.addConstraint(lambda Amy, Rob: Amy < Rob, ["Amy", "Rob"])

# "Ada finished third-to-last" → position 5 (since 7=last, 6=second-to-last, 5=third-to-last)
problem.addConstraint(lambda Ada: Ada == 5, ["Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Dan",
    "B": "Eve",
    "C": "Mya",
    "D": "Amy",
    "E": "Rob",
    "F": "Ada",
    "G": "Joe"
}

# Find who finished second-to-last (position 6)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 6:
            print(letter)
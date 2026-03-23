from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 is best)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Mya finished above Eli" → Mya's position < Eli's position
problem.addConstraint(lambda Mya, Eli: Mya < Eli, ["Mya", "Eli"])

# "Eve finished below Rob" → Rob's position < Eve's position
problem.addConstraint(lambda Rob, Eve: Rob < Eve, ["Rob", "Eve"])

# "Amy finished second" → Amy = 2
problem.addConstraint(lambda Amy: Amy == 2, ["Amy"])

# "Rob finished below Dan" → Dan's position < Rob's position
problem.addConstraint(lambda Dan, Rob: Dan < Rob, ["Dan", "Rob"])

# "Ana finished second-to-last" → position 6 (since there are 7 golfers)
problem.addConstraint(lambda Ana: Ana == 6, ["Ana"])

# "Dan finished fourth" → Dan = 4
problem.addConstraint(lambda Dan: Dan == 4, ["Dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names from the choices
choices = {
    "A": "Eve",
    "B": "Ana",
    "C": "Amy",
    "D": "Dan",
    "E": "Eli",
    "F": "Rob",
    "G": "Mya"
}

# Find who finished third (position = 3)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)